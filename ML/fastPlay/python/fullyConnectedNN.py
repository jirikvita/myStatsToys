#!/usr/bin/python

# 24.9.2024

# https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3

# ChatGPT, modified.

# TODO:
# extract features separately from each pixel's trace before concating!
# use only traces with signal above some level!

import os, sys
import shutil
from pathlib import Path

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
import numpy as np
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.initializers import RandomNormal, HeNormal
from tensorflow.keras.callbacks import Callback

import pandas as pd
#import seaborn as sns


from tensorflow.keras.layers import LSTM, Embedding, Input
from tensorflow.keras.models import Model

import matplotlib.pyplot as plt

from readData import *
from build_main_tex_from_pdfs import create_main_tex_for_pdfs


BATCH_MODE = True


def parse_batch_mode(argv):
    if ('--no-batch' in argv) or ('--interactive' in argv):
        return False
    if ('-b' in argv) or ('--batch' in argv):
        return True
    return True


def parse_maxima_only_mode(argv):
    if ('--maxima-only' in argv):
        return True
    if ('--full-run' in argv) or ('--train' in argv) or ('--no-maxima-only' in argv):
        return False
    return False


def should_show_plots():
    if os.environ.get('NN_SHOW_PLOTS', '0') == '1':
        return True
    if BATCH_MODE:
        return False
    hostname = os.environ.get('HOSTNAME', '')
    return hostname != 'zubr'


##########################################
def printWeights(model):
    for layer in model.layers:
        weights = layer.get_weights()  # Returns a list of weights (and biases)
        print(f"Layer {layer.name}:")
        
        # Check if the layer has weights
        if weights:
            print("Weights:", weights[0].shape)  # Print weights shape
            if len(weights) > 1:  # Some layers may not have biases
                print("Biases:", weights[1].shape)  # Print biases shape
        else:
            print("No weights for this layer.")
            """
            # Print all trainable weights
for layer in model.layers:
    print(f"Layer {layer.name} trainable weights:")
    for weight in layer.trainable_weights:
        print(weight.name, weight.shape)

# Print all non-trainable weights
for layer in model.layers:
    print(f"Layer {layer.name} non-trainable weights:")
    for weight in layer.non_trainable_weights:
        print(weight.name, weight.shape)

        """


##########################################
def _sanitize_name(name):
    return str(name).replace('/', '_').replace(':', '_').replace(' ', '_')


##########################################
def plot_model_params_2d(model, tag, stage, cmap='turbo'):
    """Save 2D heatmaps of model weights and biases for a given training stage."""
    print(f'Plotting model parameter matrices for stage "{stage}" (tag "{tag}")...')
    n_weights = 0
    n_biases = 0

    for layer in model.layers:
        params = layer.get_weights()
        if not params:
            continue

        for ip, param in enumerate(params):
            arr = np.asarray(param)
            pname = _sanitize_name(f'{layer.name}_p{ip}')

            if arr.ndim == 1:
                # Plot 1D bias-like vectors as 1xN matrices for consistent heatmap style.
                fig = plt.figure(figsize=(10, 2.8))
                ax = fig.add_subplot(111)
                im = ax.imshow(arr.reshape(1, -1), aspect='auto', interpolation='nearest', cmap=cmap)
                fig.colorbar(im, ax=ax)
                ax.set_title(f'biases2d {layer.name} param#{ip} ({stage})')
                ax.set_xlabel('Index')
                ax.set_ylabel('Row')
                out_png = f'biases2d_{pname}_{stage}{tag}.png'
                out_pdf = f'biases2d_{pname}_{stage}{tag}.pdf'
                fig.tight_layout()
                fig.savefig(out_png)
                fig.savefig(out_pdf)
                plt.close(fig)
                n_biases += 1
                continue

            if arr.ndim >= 2:
                arr2 = arr if arr.ndim == 2 else arr.reshape(arr.shape[0], -1)
                fig = plt.figure(figsize=(10, 6))
                ax = fig.add_subplot(111)
                im = ax.imshow(arr2, aspect='auto', interpolation='nearest', cmap=cmap)
                fig.colorbar(im, ax=ax)
                ax.set_title(f'weights2d {layer.name} param#{ip} ({stage})')
                ax.set_xlabel('Column')
                ax.set_ylabel('Row')
                out_png = f'weights2d_{pname}_{stage}{tag}.png'
                out_pdf = f'weights2d_{pname}_{stage}{tag}.pdf'
                fig.tight_layout()
                fig.savefig(out_png)
                fig.savefig(out_pdf)
                plt.close(fig)
                n_weights += 1

    print(f'Saved {n_weights} weight heatmap(s) and {n_biases} bias heatmap(s) for stage "{stage}".')

##########################################

def plotBias(predictedY,trueY, **kwargs):
    eBias = []
    xmaxBias = []

    ePreds = []
    eTrues = []

    xmaxPreds = []
    xmaxTrues = []
    
    for y,ytrue in zip(predictedY,trueY):
        ePred,xmaxPred = y[0], y[1]
        eTrue,xmaxTrue = ytrue[0], ytrue[1]
        #print('-------------------------------------------')
        #print(f'E:    true: {eTrue:10.1f}    predicted: {ePred:10.1f}')
        #print(f'Xmax: true: {xmaxTrue:10.1f} predicted: {xmaxPred:10.1f}')
        de = ePred - eTrue
        dxmax = xmaxPred - xmaxTrue
        #eBias.append(de)
        #xmaxBias.append(dxmax)
        eBias.append(de / eTrue)
        xmaxBias.append(dxmax / xmaxTrue)

        ePreds.append(ePred)
        eTrues.append(eTrue)
        xmaxPreds.append(xmaxPred)
        xmaxTrues.append(xmaxTrue)


    df = pd.DataFrame({
        'eTrue': eTrues,
        'eBias': eBias,
        'ePred': ePreds,
        'xmaxTrue': xmaxTrues,
        'xmaxBias' : xmaxBias,
        'xmaxPred' : xmaxPreds 
    })
    n_events = max(1, len(eTrues))
    # Keep dense scatters readable by scaling alpha with sample size.
    scatter_alpha = min(max(0.01, 2000.0 / float(n_events)), 0.8)

    corr_e = float(np.corrcoef(eTrues, ePreds)[0, 1]) if len(eTrues) > 1 else float('nan')
    corr_x = float(np.corrcoef(xmaxTrues, xmaxPreds)[0, 1]) if len(xmaxTrues) > 1 else float('nan')
    
    
    # Create a figure with 1 row and 2 columns of subplots
    plt.figure(figsize=(10, 8))
    
    # First subplot (left)
    plt.subplot(2, 2, 1)
    plt.hist(eBias, bins=25, color='red', alpha=0.7)
    #plt.title('logE bias')
    plt.xlabel(r'logE: (predicted-true)/true')
    
    # Second subplot (right)
    plt.subplot(2, 2, 3)
    plt.hist(xmaxBias, bins=25, color='blue', alpha=0.7)
    #plt.title('Xmax bias')
    plt.xlabel(r'$X_{max}$: (predicted-true)/true')
    # Adjust the layout to prevent overlap
    #plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    plt.subplots_adjust(left=0.1)

    plt.subplot(2, 2, 2)
    plt.scatter(eTrues, ePreds, c='red', s=5, alpha=scatter_alpha)
    plt.plot([16, 21], [16, 21], 'k--', linewidth=1)
    plt.xlabel('true logE')
    plt.ylabel('predicted logE')
    #plt.title('logE scatter')
    plt.xlim(16, 21)
    plt.ylim(16, 21)
    plt.subplots_adjust(bottom=0.1)
    plt.subplots_adjust(left=0.1)
    #plt.tight_layout()
    print(f'E correlation factor: {corr_e:.2f}')
    
    plt.subplot(2, 2, 4)
    plt.scatter(xmaxTrues, xmaxPreds, c='blue', s=5, alpha=scatter_alpha)
    plt.plot([150, 1200], [150, 1200], 'k--', linewidth=1)
    plt.xlabel(r'true $X_{max}$')
    plt.ylabel(r'predicted $X_{max}$')
    #plt.title('X_{max} scatter')
    plt.xlim(150, 1200)
    plt.ylim(150, 1200)
    plt.subplots_adjust(bottom=0.1)
    print(f'Xmax correlation factor: {corr_x:.2f}')

    #plt.subplots_adjust()
    #plt.tight_layout()

    # Show the plots
    tag = ''
    if 'tag' in kwargs:
        tag = kwargs['tag']
    subset_label = kwargs.get('subset_label', '').strip().upper()
    trace_max_cut = kwargs.get('trace_max_cut', None)
    subset_prefix = f'{subset_label} ' if subset_label else ''
    if trace_max_cut is None:
        cut_suffix = ' | amp cut: none'
    else:
        cut_suffix = f' | amp cut >= {float(trace_max_cut):.2f}'

    print(f'Plotting bias summary panels for tag "{tag}" on {len(eTrues)} events:')
    print('- logE bias histogram')
    print('- Xmax bias histogram')
    print('- logE true vs predicted scatter')
    print('- Xmax true vs predicted scatter')

    plt.subplot(2, 2, 1)
    plt.title(f'{subset_prefix}logE bias')
    plt.subplot(2, 2, 3)
    plt.title(f'{subset_prefix}Xmax bias')
    plt.subplot(2, 2, 2)
    plt.title(f'{subset_prefix}logE true vs predicted (corr={corr_e:.2f}){cut_suffix}')
    plt.subplot(2, 2, 4)
    plt.title(f'{subset_prefix}Xmax true vs predicted (corr={corr_x:.2f}){cut_suffix}')
    
    plt.savefig(f'biases{tag}.png')
    plt.savefig(f'biases{tag}.pdf')
    print(f'Saved bias plots: biases{tag}.png and biases{tag}.pdf')

    print(f'Plotting 2D-histogram versions of scatter panels for tag "{tag}" (50x50 bins, rainbow palette).')
    fig2 = plt.figure(figsize=(12, 5))

    ax = fig2.add_subplot(1, 2, 1)
    h = ax.hist2d(eTrues, ePreds, bins=(50, 50), range=[[16, 21], [16, 21]], cmap='rainbow')
    fig2.colorbar(h[3], ax=ax)
    ax.plot([16, 21], [16, 21], 'k--', linewidth=1)
    ax.set_xlim(16, 21)
    ax.set_ylim(16, 21)
    ax.set_xlabel('true logE')
    ax.set_ylabel('predicted logE')
    ax.set_title(f'{subset_prefix}logE true vs predicted (corr={corr_e:.2f}){cut_suffix}')

    ax = fig2.add_subplot(1, 2, 2)
    h = ax.hist2d(xmaxTrues, xmaxPreds, bins=(50, 50), range=[[150, 1200], [150, 1200]], cmap='rainbow')
    fig2.colorbar(h[3], ax=ax)
    ax.plot([150, 1200], [150, 1200], 'k--', linewidth=1)
    ax.set_xlim(150, 1200)
    ax.set_ylim(150, 1200)
    ax.set_xlabel(r'true $X_{max}$')
    ax.set_ylabel(r'predicted $X_{max}$')
    ax.set_title(f'{subset_prefix}Xmax true vs predicted (corr={corr_x:.2f}){cut_suffix}')

    fig2.tight_layout()
    fig2.savefig(f'biases_scatter2d{tag}.png')
    fig2.savefig(f'biases_scatter2d{tag}.pdf')
    print(f'Saved 2D-hist scatter plots: biases_scatter2d{tag}.png and biases_scatter2d{tag}.pdf')

    if should_show_plots():
        plt.show()
    
##########################################
def concatData(data):
    vals = []
    for dss in data:
        for ds in dss:
            vals.append(ds)
    return vals

##########################################
def ReadAndParseData(infname, i1, i2, **kwargs):
    Data = readData(infname, i1, i2, **kwargs)

    trace_max_cut = kwargs.get('trace_max_cut', None)
    plot_trace_max_hist = kwargs.get('plot_trace_max_hist', False)
    trace_max_hist_tag = kwargs.get('trace_max_hist_tag', '')
    save_trace_max_txt = kwargs.get('save_trace_max_txt', True)

    ys = []
    xs = []
    event_trace_maxima = []
    n_below_trace_max_cut = 0
    for data in Data:
        traces = data[1]
        trace_maxima = [max(trace) for trace in traces if len(trace) > 0]
        event_trace_max = max(trace_maxima) if len(trace_maxima) > 0 else 0.0
        event_trace_maxima.append(event_trace_max)

        if trace_max_cut is not None and event_trace_max < trace_max_cut:
            n_below_trace_max_cut = n_below_trace_max_cut + 1
            continue

        logE = data[0]['logE']
        Xmax = data[0]['Xmax']
        # to rething!
        # maybe later extract features from each trace separately
        # and not from concatenated data?
        # or does not matter?
        xxs = concatData(traces)
        if len(xxs) > 0:
            xs.append(xxs)
            ys.append([logE, Xmax])

    # Single source of truth: these are the per-event maxima used for both txt export and histogram x-values.
    maxima_for_plot = np.asarray(event_trace_maxima, dtype=float)

    if save_trace_max_txt:
        trace_max_txt = Path(f'event_trace_maxima{trace_max_hist_tag}.txt')
        with trace_max_txt.open('w') as out:
            out.write('# event_index event_trace_max\n')
            for ievt, vmax in enumerate(maxima_for_plot):
                out.write(f'{ievt} {float(vmax):.10g}\n')
        print(f'Saved full event-trace-max list to {trace_max_txt} ({len(maxima_for_plot)} rows).')

    if plot_trace_max_hist and len(maxima_for_plot) > 0:
        # Plot exactly the same per-event maxima values that are written to txt.
        print("event_trace_maxima[0:100]: ", event_trace_maxima[0:100])
        print('Plotting event trace-max histogram before cut:')
        print(f'- one entry per event maxima list size: {len(maxima_for_plot)}')
        print(f'- histogram source entries: {len(maxima_for_plot)}')
        print(f'- source min/max: {float(np.min(maxima_for_plot))} / {float(np.max(maxima_for_plot))}')
        hist_bins = 100
        hist_range = (0.0, 40.0)
        in_range = int(np.sum((maxima_for_plot >= hist_range[0]) & (maxima_for_plot <= hist_range[1])))
        print(f'- entries inside plotting x-range [{hist_range[0]}, {hist_range[1]}]: {in_range}')
        counts, edges = np.histogram(maxima_for_plot, bins=hist_bins, range=hist_range)
        print(f'- histogram bins: {len(counts)}; total counted in [0, 40]: {int(np.sum(counts))}')
        print('- semantics: x-axis = maxima values, y-axis = frequency (counts per bin)')

        hist_pairs_txt = Path(f'event_trace_max_hist_pairs{trace_max_hist_tag}.txt')
        with hist_pairs_txt.open('w') as out:
            out.write('# bin_i x_center y_count x_left x_right\n')
            for ibin, ycount in enumerate(counts):
                x_left = float(edges[ibin])
                x_right = float(edges[ibin + 1])
                x_center = 0.5 * (x_left + x_right)
                out.write(f'{ibin} {x_center:.10g} {int(ycount)} {x_left:.10g} {x_right:.10g}\n')
        print(f'Saved histogram bin pairs to {hist_pairs_txt} ({len(counts)} bins).')

        if trace_max_cut is not None:
            print(f'- cut marker shown at event_max = {trace_max_cut}')

        plt.figure(figsize=(10, 6))
        plt.hist(maxima_for_plot, bins=hist_bins, range=hist_range, color='steelblue', alpha=0.8)
        plt.xlim(hist_range[0], hist_range[1])
        if trace_max_cut is not None:
            plt.axvline(trace_max_cut, color='red', linestyle='--', linewidth=2,
                        label=f'cut = {trace_max_cut}')
            plt.legend()
        plt.xlabel('Event max over all trace maxima')
        plt.ylabel('Number of events (counts)')
        plt.title('Event Trace Maxima Before Cut')
        plt.savefig(f'event_trace_max_before_cut{trace_max_hist_tag}.png')
        plt.savefig(f'event_trace_max_before_cut{trace_max_hist_tag}.pdf')
        print(
            'Saved trace-max histogram: '
            f'event_trace_max_before_cut{trace_max_hist_tag}.png and '
            f'event_trace_max_before_cut{trace_max_hist_tag}.pdf'
        )
        # Save-only mode for amplitude histogram: do not open GUI windows.
        plt.close()

    if trace_max_cut is not None:
        print(f'Applied event trace-max cut: event_max >= {trace_max_cut}')
        print(f'Events rejected by trace-max cut: {n_below_trace_max_cut}')
    print(f'Events kept after trace-max cut and parsing: {len(xs)}')

    debug = 0
    if 'debug' in kwargs:
        debug = kwargs['debug']
    if debug:
        print('-----------------------------------------------')
        print(xs)
        print('-----------------------------------------------')
        print(ys)
        print('-----------------------------------------------')
        for x in xs:
            print(len(x))
        print('-----------------------------------------------')
        for y in ys:
            print(len(y))
    
    rows = len(xs)
    if rows == 0:
        raise ValueError('No parsed events survived filters; try another ascii input file or relax selection cuts')
    cols = len(xs[0])
    X = np.array(xs, dtype=float).reshape(rows, cols)
    rows = len(ys)
    cols = len(ys[0])
    Y = np.array(ys).reshape(rows, cols)
    return X, Y


##########################################
class EveryNEpochLogger(Callback):
    def __init__(self, n=5):
        super().__init__()
        self.n = max(1, int(n))

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        epoch_num = epoch + 1
        total_epochs = self.params.get('epochs', epoch_num)
        should_print = (epoch_num == 1) or (epoch_num % self.n == 0) or (epoch_num == total_epochs)
        if not should_print:
            return

        loss = logs.get('loss', float('nan'))
        mae = logs.get('mae', float('nan'))
        val_loss = logs.get('val_loss', float('nan'))
        val_mae = logs.get('val_mae', float('nan'))
        print(
            f'Epoch {epoch_num}/{total_epochs} '
            f'- loss: {loss:.6f} - mae: {mae:.6f} '
            f'- val_loss: {val_loss:.6f} - val_mae: {val_mae:.6f}'
        )

##########################################
def main(argv):
    global BATCH_MODE
    BATCH_MODE = parse_batch_mode(argv)
    maxima_only_mode = parse_maxima_only_mode(argv)
    print(f'Batch mode: {BATCH_MODE} (default on; use --no-batch or --interactive to disable)')
    print('Maxima-only mode: '
          f'{maxima_only_mode} '
            '(default off; use --maxima-only to save maxima artifacts and exit early)')

    # No event-level cuts at read-in: keep all events that parse correctly.
    minSignal = -1
    trace_max_cut = 7.
    
    # central vals and sigma around them to accept
    restrictions = {}

    # HACK!
    #restrictions = {}
    #restrictions = restrictions1
    # Resolve input file robustly for runs from different working directories.
    script_dir = Path(__file__).resolve().parent
    candidate_inputs = [
        Path.cwd() / 'ascii.txt',
        Path('ascii.txt'),
        script_dir / 'ascii.txt',
        script_dir.parent / 'ascii.txt',
    ]
    infname = None
    for candidate in candidate_inputs:
        if candidate.exists():
            infname = str(candidate)
            break
    if infname is None:
        raise FileNotFoundError('ascii.txt not found in working dir or script paths')
    print(f'Using ascii input file: {Path(infname).resolve()}')

    i1 = 0
    i2 = -1
    debug = 0
    verb = 1000
    plot_meta_histos = True
    print('Metadata shower-parameter 2D figures: always generated and saved')
    X, Y = ReadAndParseData(infname, i1, i2, debug=debug, verb=verb,
                            plotmetahistos=plot_meta_histos, skip='', minSignal=minSignal,
                            restrictions=restrictions,
                            trace_max_cut=trace_max_cut,
                            plot_trace_max_hist=True,
                            save_trace_max_txt=True,
                            trace_max_hist_tag='_all_events')

    if maxima_only_mode:
        results_dir = Path('results') / 'event_maxima_only'
        results_dir.mkdir(parents=True, exist_ok=True)
        maxima_artifacts = [
            'event_trace_max_before_cut_all_events.png',
            'event_trace_max_before_cut_all_events.pdf',
            'event_trace_maxima_all_events.txt',
            'event_trace_max_hist_pairs_all_events.txt',
        ]
        moved = 0
        for artifact_name in maxima_artifacts:
            artifact = Path(artifact_name)
            if artifact.is_file():
                shutil.move(str(artifact), str(results_dir / artifact.name))
                moved += 1
        print(f'Maxima-only mode complete. Moved {moved} artifact(s) to {results_dir.resolve()}')
        return

    # Split after full read to avoid any read-phase selection bias.
    n_events_all = len(X)
    if n_events_all < 2:
        raise ValueError('Need at least 2 events to build train/test split')
    test_fraction = 0.2
    n_test = max(1, int(test_fraction * n_events_all))
    n_test = min(n_test, n_events_all - 1)
    rng = np.random.default_rng(42)
    indices = rng.permutation(n_events_all)
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]

    trainX = X[train_indices]
    trainY_raw = Y[train_indices]
    testX = X[test_indices]
    trueY_raw = Y[test_indices]

    # Standardize target features (logE, Xmax) using TRAIN subset stats only
    # so both outputs contribute more fairly in the MSE loss.
    y_mean = np.mean(trainY_raw, axis=0)
    y_std = np.std(trainY_raw, axis=0)
    y_std_safe = np.where(y_std > 0.0, y_std, 1.0)
    trainY = (trainY_raw - y_mean) / y_std_safe
    trueY = (trueY_raw - y_mean) / y_std_safe
    print(f'Target standardization (train stats): mean={y_mean}, std={y_std_safe}')

    """
    Recurrent Neural Networks (RNNs) & LSTMs for Sequential Data
    For time series or textual data, RNNs, Long Short-Term Memory Networks (LSTMs), and Transformers can automatically learn temporal features.
    Once trained, these networks can provide feature representations from their hidden states or intermediate layers.
    """

    n_events = len(trainX)  # Number of samples in the training dataset
    print(f'Number of events: {n_events}')
    input_dim = len(trainX[0])      # Number of original input features

    print(f'Read events       : {len(X)}')
    print(f'Train events      : {len(trainX)}')
    print(f'Test events       : {len(testX)}')
    print(f'Original features : {input_dim}')

    # desired features:
    Nfeat = 64
    print(f'Desired transformed features : {Nfeat}')

    trainX_reshaped = np.expand_dims(trainX, axis=1)

    # Build an end-to-end model so the LSTM feature extractor is trained by regression loss.
    input_layer = Input(shape=(1, input_dim))
    lstm_out = LSTM(Nfeat, return_sequences=False)(input_layer)
    feature_extractor = Model(inputs=input_layer, outputs=lstm_out)
    print("Planned extracted features shape:", (n_events, Nfeat))


    """
    # other options:

    from sklearn.decomposition import PCA

    # Apply PCA for feature extraction
    pca = PCA(n_components=10)
    reduced_features = pca.fit_transform(input_data)

    from tensorflow.keras.layers import GlobalAveragePooling2D

    # Add global average pooling layer
    x = GlobalAveragePooling2D()(feature_maps)

    """

    #####################
    # Build the model
    print('Building model architecture...')
    
    # activations: relu, sigmoid, linear
    # kernel_initializer=RandomNormal(mean=0.0, stddev=0.05), bias_initializer='zeros'
    #, input_shape=(32,)),

    N1, N2, N3, N4 = 256, 128, 128, 64
    print(f'Model layer plan: input -> {N1} -> {N2} -> {N3} -> {N4} -> 2 outputs')
    x = Dense(N1, activation='relu')(lstm_out)                # First hidden layer
    x = BatchNormalization()(x)                               # Batch normalization of the output
    if N2 > 0:
        x = Dense(N2, activation='relu')(x)                   # Second hidden layer
    if N3 > 0:
        x = Dense(N3, activation='relu')(x)                   # Third hidden layer
    if N4 > 0:
        x = Dense(N4, activation='relu')(x)                   # Fourth hidden layer
    output = Dense(2, activation='linear')(x)                 # Output layer (2 outputs, no activation for regression)

    model = Model(inputs=input_layer, outputs=output)
    print('Model architecture successfully built.')

    #####################
    # Compile the model
    # other examples:
    # loss='binary_crossentropy', metrics=['accuracy']
    # other optimizers: SGD, default learning rate 0.01
    # Adam: 0.0001


    #####################
    # Training parameters
    learning_rate = 0.0002 # learning rate
    epochs = 100           # Number of epochs for training
    batch_size = 32        # batch size
        
    optimizer = Adam(learning_rate=learning_rate)  # Change learning rate here
    #optimizer = SGD(learning_rate=0.01)  # Change learning rate here

    slearning_rate = str(learning_rate).replace('.','p')
    mtag = f'_LSTM_i1_{i1}_i2_{i2}_epochs_{epochs}_lrate_{slearning_rate}_Nfeat_{Nfeat}_Neurons_{N1}_{N2}_{N3}_{N4}'

    print('Model summary:')
    model.summary()
    total_params = model.count_params()
    print(f"Total number of parameters: {total_params}")

    model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])

    # Save model parameter heatmaps before any training updates.
    plot_model_params_2d(model, mtag, stage='pretrain', cmap='turbo')

    #####################
    # Train the model
    logger_every_5_epochs = EveryNEpochLogger(n=5)
    history = model.fit(
        trainX_reshaped,
        trainY,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        verbose=0,
        callbacks=[logger_every_5_epochs],
    )
    print('Done training!')
    # Save model parameter heatmaps after training updates.
    plot_model_params_2d(model, mtag, stage='posttrain', cmap='turbo')
    #print('Printing the model...')
    #printWeights(model)
    
    print('Going to test the trained model...')
    if trace_max_cut is None:
        trace_cut_tag = 'none'
    else:
        trace_cut_tag = str(trace_max_cut).replace('.', 'p')
    results_tag = (
        f'neurons_{N1}_{N2}_{N3}_{N4}_lr_{slearning_rate}_bs_{batch_size}'
        f'_traceMaxCut_{trace_cut_tag}'
    )
    results_dir = Path('results') / results_tag
    results_dir.mkdir(parents=True, exist_ok=True)

    print('Plotting loss function vs epoch...')
    train_loss = history.history.get('loss', [])
    val_loss = history.history.get('val_loss', [])
    if len(train_loss):
        plt.figure(figsize=(10, 6))
        xvals = np.arange(1, len(train_loss) + 1)
        plt.plot(xvals, train_loss, color='blue', linewidth=1.5, label='train loss')
        if len(val_loss):
            plt.plot(xvals, val_loss, color='green', linewidth=1.5, label='validation loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss (MSE)')
        plt.title('Loss vs Epoch')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'training_loss_vs_epoch{mtag}.png')
        plt.savefig(f'training_loss_vs_epoch{mtag}.pdf')
        print(f'Saved loss-vs-epoch plots: training_loss_vs_epoch{mtag}.png and training_loss_vs_epoch{mtag}.pdf')
        if should_show_plots():
            plt.show()
        else:
            plt.close()

    ##########################################
    # Plot performance on the train datase:
    print('Plotting TRAIN performance diagnostics (bias/scatter panels)...')
    train_predictedY_std = model.predict(trainX_reshaped)
    train_predictedY = train_predictedY_std * y_std_safe + y_mean
    plotBias(train_predictedY, trainY_raw, tag = mtag + '_train', subset_label='train', trace_max_cut=trace_max_cut)
    
    ##########################################
    # Predict on held-out test split sampled from the full read dataset.
    print(f'Read test events  : {len(testX)}')
    
    testX_reshaped = np.expand_dims(testX, axis=1)
    predictedY_std = model.predict(testX_reshaped)
    predictedY = predictedY_std * y_std_safe + y_mean
    print(f"Predicted output: {predictedY}")

    # save
    #print('Saving the model...')
    #model.save(f'model_{mtag}.keras')

    # load in usage:
    # from tensorflow.keras.models import load_model
    # Load the model
    # model = load_model('model.keras')

    print('Plotting TEST performance diagnostics (bias/scatter panels)...')
    plotBias(predictedY, trueY_raw, tag = mtag + '_test', subset_label='test', trace_max_cut=trace_max_cut)

    # Move run outputs into results/<neurons+lr+bs-tag>/
    artifact_patterns = [
        f'biases{mtag}_*.png',
        f'biases{mtag}_*.pdf',
        f'biases_scatter2d{mtag}_*.png',
        f'biases_scatter2d{mtag}_*.pdf',
        f'weights2d_*{mtag}.png',
        f'weights2d_*{mtag}.pdf',
        f'biases2d_*{mtag}.png',
        f'biases2d_*{mtag}.pdf',
        f'training_loss_vs_epoch{mtag}.png',
        f'training_loss_vs_epoch{mtag}.pdf',
        'event_trace_max_before_cut_all_events.png',
        'event_trace_max_before_cut_all_events.pdf',
        'event_trace_maxima_all_events.txt',
        'event_trace_max_hist_pairs_all_events.txt',
    ]
    moved = 0
    for pattern in artifact_patterns:
        for artifact in Path('.').glob(pattern):
            if artifact.is_file():
                shutil.move(str(artifact), str(results_dir / artifact.name))
                moved += 1
    print(f'Moved {moved} artifact(s) to {results_dir.resolve()}')

    try:
        main_tex, n_pdfs = create_main_tex_for_pdfs(results_dir)
        print(f'Created LaTeX include file {main_tex} with {n_pdfs} PDF(s).')
    except Exception as ex:
        print(f'WARNING: failed to create main.tex from PDFs in {results_dir}: {ex}')


###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################
