
TARGET=BMI_index
ROOT=`root-config --libs --cflags` -lMinuit2
CXX=g++  -std=c++11

all:$(TARGET)

$(TARGET):%:%.cxx ToyCovariance.h ToyCovariance.C
	$(CXX) -o $@ $< -I$(WORK)/include $(ROOT)

clean:
	rm $(TARGET) *.eps


