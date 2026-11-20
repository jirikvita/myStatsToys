#!/usr/bin/env python3
"""Generate a shuffled Japanese vocabulary worksheet.

Run ``python3 genKanjiTestPdf.py`` to write kanji_test.tex and kanji_test.pdf
in the current directory. Requires XeLaTeX, xeCJK and the IPAexGothic font.
The entries "deimasu", "chii" and "furu" are interpreted as demasu,
chiisai and furui respectively. Each unique vocabulary entry is shown with
its hiragana reading and a blank line for writing.
"""

import argparse
from pathlib import Path
import random
import shutil
import subprocess
import tempfile


romanji = ["kakarimasu", "nemasu", "tabemasu", "nomimasu",
           "kikimasu", "oyogimasu", "nemasu", "okimasu",
           "sundeimasu", "suwarimasu", "kaerimasu", "ikimasu", "kaimasu",
           "kimasu", "yasumimasu", "hikkoshimasu", "onegaishimasu", 
           "mimasu", "yomimasu", "hanashimasu", "deimasu", "tsukurimasu",
           "abimasu", "asobimasu", "toiimasu", "wakarimasu", "dekakemasu",
           "aimasu","tanoshii", "suki", "hoshii",
           "akimasu", "akemasu",

           "sai", "ani", "ane", "otouto", "imouto",
           "chichi", "haha",
           "otouto", "imouto", "musuko", "musume",
           "kodomo", "tomodachi", "sensei", "gakusei",
           "daigaku", "gakkou", "ie", "machi", "Tokyo", "Osaka", "Kyoto",
           "eki", "kaisatsu", 
           "toui", "chikai", "ato",
           "chii", "ookii", "takai", "furu", "atarashii", "omoshiroi", "tanoshii",
           "sukoshi",
           
           "aoi", "akai", "kuroi", "shiroi", "midori",

           "shusshin", "yama", "kawa", "guchi", "ta", "ocha", "hon",
           "haru", "natsu", "aki", "fuyu",
           "hi", "getsu", 
           "hana",
           "nichiyoubi", "getsuyoubi", "kayoubi", "suiyoubi", "mokuyoubi", "kinyoubi", "doyoubi",

           "harenohi", "amenohi", "kumorinohi", "yukinohi",
           "denwa", "densha", "kutsu", "kasa", "kaban", "isogashii", "itsu",
           "hondana", "hontooni",

           "watashi", "nan", "ji", "denwabangou", "samui", "shinbun",

           "ichi", "ni", "san", "shi", "go", "roku", "shichi", "hachi", "kyuu", "juu",
           "hyaku", "sen", "man", "en","namae", "e", "kouen", "eiga", "hito", 
            "tanjoubi", "ashita", "kyou", "ban" ,"yoru", "asa",
            "ima", "shuumatsu", "raishuu", "konshuu", "raigetsu",
            "maishuu", "maigetsu", "maiasa", "maiban", "konban", "mainichi",
            "juppun"

           ]


japanese = {
    "kakarimasu": ("掛かります", "かかります"),
    "nemasu": ("寝ます", "ねます"), "tabemasu": ("食べます", "たべます"),
    "nomimasu": ("飲みます", "のみます"), "kikimasu": ("聞きます", "ききます"),
    "oyogimasu": ("泳ぎます", "およぎます"), "okimasu": ("起きます", "おきます"),
    "sundeimasu": ("住んでいます", "すんでいます"),
    "suwarimasu": ("座ります", "すわります"), "kaerimasu": ("帰ります", "かえります"),
    "ikimasu": ("行きます", "いきます"), "kaimasu": ("買います", "かいます"),
    "kimasu": ("来ます", "きます"), "yasumimasu": ("休みます", "やすみます"),
    "hikkoshimasu": ("引っ越します", "ひっこします"),
    "onegaishimasu": ("お願いします", "おねがいします"),
    "mimasu": ("見ます", "みます"), "yomimasu": ("読みます", "よみます"),
    "hanashimasu": ("話します", "はなします"), "deimasu": ("出ます", "でます"),
    "tsukurimasu": ("作ります", "つくります"), "abimasu": ("浴びます", "あびます"),
    "asobimasu": ("遊びます", "あそびます"), "toiimasu": ("と言います", "といいます"),
    "wakarimasu": ("分かります", "わかります"), "dekakemasu": ("出かけます", "でかけます"),
    "aimasu": ("会います", "あいます"), "tanoshii": ("楽しい", "たのしい"),
    "suki": ("好き", "すき"), "hoshii": ("欲しい", "ほしい"),
    "sai": ("歳", "さい"), "ani": ("兄", "あに"), "ane": ("姉", "あね"),
    "otouto": ("弟", "おとうと"), "imouto": ("妹", "いもうと"),
    "chichi": ("父", "ちち"), "haha": ("母", "はは"),
    "musuko": ("息子", "むすこ"), "musume": ("娘", "むすめ"),
    "kodomo": ("子供", "こども"), "tomodachi": ("友達", "ともだち"),
    "sensei": ("先生", "せんせい"), "gakusei": ("学生", "がくせい"),
    "daigaku": ("大学", "だいがく"), "gakkou": ("学校", "がっこう"),
    "ie": ("家", "いえ"), "machi": ("町", "まち"), "Tokyo": ("東京", "とうきょう"),
    "Osaka": ("大阪", "おおさか"), "Kyoto": ("京都", "きょうと"),
    "eki": ("駅", "えき"), "kaisatsu": ("改札", "かいさつ"),
    "toui": ("遠い", "とおい"), "chikai": ("近い", "ちかい"), "ato": ("後", "あと"),
    "chii": ("小さい", "ちいさい"), "ookii": ("大きい", "おおきい"),
    "takai": ("高い", "たかい"), "furu": ("古い", "ふるい"),
    "atarashii": ("新しい", "あたらしい"), "omoshiroi": ("面白い", "おもしろい"),
    "sukoshi": ("少し", "すこし"), "aoi": ("青い", "あおい"),
    "akai": ("赤い", "あかい"), "kuroi": ("黒い", "くろい"),
    "shiroi": ("白い", "しろい"), "midori": ("緑", "みどり"),
    "shusshin": ("出身", "しゅっしん"), "yama": ("山", "やま"),
    "kawa": ("川", "かわ"), "guchi": ("口", "くち"), "ta": ("田", "た"),
    "ocha": ("お茶", "おちゃ"), "hon": ("本", "ほん"), "haru": ("春", "はる"),
    "natsu": ("夏", "なつ"), "aki": ("秋", "あき"), "fuyu": ("冬", "ふゆ"),
    "hi": ("日", "ひ"), "getsu": ("月", "げつ"), "hana": ("花", "はな"),
    "nichiyoubi": ("日曜日", "にちようび"), "getsuyoubi": ("月曜日", "げつようび"),
    "kayoubi": ("火曜日", "かようび"), "suiyoubi": ("水曜日", "すいようび"),
    "mokuyoubi": ("木曜日", "もくようび"), "kinyoubi": ("金曜日", "きんようび"),
    "doyoubi": ("土曜日", "どようび"),
    "harenohi": ("晴れの日", "はれのひ"), "amenohi": ("雨の日", "あめのひ"),
    "kumorinohi": ("曇りの日", "くもりのひ"), "yukinohi": ("雪の日", "ゆきのひ"),
    "denwa": ("電話", "でんわ"), "densha": ("電車", "でんしゃ"),
    "kutsu": ("靴", "くつ"), "kasa": ("傘", "かさ"), "kaban": ("鞄", "かばん"),
    "isogashii": ("忙しい", "いそがしい"), "itsu": ("何時", "いつ"),
    "hondana": ("本棚", "ほんだな"), "hontooni": ("本当に", "ほんとうに"),
    "akimasu": ("開きます", "あきます"), "akemasu": ("開けます", "あけます"),
    "watashi": ("私", "わたし"), "nan": ("何", "なん"), "ji": ("時", "じ"),
    "denwabangou": ("電話番号", "でんわばんごう"), "samui": ("寒い", "さむい"),
    "shinbun": ("新聞", "しんぶん"),
    "ichi": ("一", "いち"), "ni": ("二", "に"), "san": ("三", "さん"),
    "shi": ("四", "し"), "go": ("五", "ご"), "roku": ("六", "ろく"),
    "shichi": ("七", "しち"), "hachi": ("八", "はち"), "kyuu": ("九", "きゅう"),
    "juu": ("十", "じゅう"), "hyaku": ("百", "ひゃく"), "sen": ("千", "せん"),
    "man": ("万", "まん"), "en": ("円", "えん"), "namae": ("名前", "なまえ"),
    "e": ("絵", "え"), "kouen": ("公園", "こうえん"), "eiga": ("映画", "えいが"),
    "hito": ("人", "ひと"), "tanjoubi": ("誕生日", "たんじょうび"),
    "ashita": ("明日", "あした"), "kyou": ("今日", "きょう"),
    "ban": ("晩", "ばん"), "yoru": ("夜", "よる"), "asa": ("朝", "あさ"),
    "ima": ("今", "いま"), "shuumatsu": ("週末", "しゅうまつ"),
    "raishuu": ("来週", "らいしゅう"), "konshuu": ("今週", "こんしゅう"),
    "raigetsu": ("来月", "らいげつ"), "maishuu": ("毎週", "まいしゅう"),
    "maigetsu": ("毎月", "まいげつ"), "maiasa": ("毎朝", "まいあさ"),
    "maiban": ("毎晩", "まいばん"), "konban": ("今晩", "こんばん"),
    "mainichi": ("毎日", "まいにち"), "juppun": ("十分", "じゅっぷん"),
}


def make_latex():
    # Repeated entries in romanji represent the same vocabulary item.
    words = list(dict.fromkeys(romanji))
    random.shuffle(words)
    lines = [
        r"\noindent " + japanese[word][0] + "（" + japanese[word][1] + "）"
        + r"\quad\hrulefill\par\vspace{1em}"
        for word in words
    ]
    return "\n".join([
        r"\documentclass[12pt]{article}",
        r"\usepackage[margin=2cm]{geometry}",
        r"\usepackage{xeCJK}",
        r"\setCJKmainfont{IPAexGothic}",
        r"\setlength{\parindent}{0pt}",
        r"\begin{document}",
        *lines,
        r"\end{document}",
        "",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("kanji_test.pdf"),
        help="output PDF path (the LaTeX source is saved alongside it)",
    )
    args = parser.parse_args()
    if args.output.suffix.lower() != ".pdf":
        parser.error("output must have a .pdf extension")

    tex_path = args.output.with_suffix(".tex").resolve()
    pdf_path = args.output.resolve()
    tex_path.write_text(make_latex(), encoding="utf-8")
    try:
        with tempfile.TemporaryDirectory() as build_dir:
            subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                 f"-output-directory={build_dir}", str(tex_path)],
                check=True,
            )
            shutil.copyfile(Path(build_dir) / tex_path.with_suffix(".pdf").name, pdf_path)
    except FileNotFoundError as error:
        parser.exit(1, f"Could not run XeLaTeX: {error}\n")
    except subprocess.CalledProcessError:
        parser.exit(1, f"XeLaTeX failed; LaTeX source saved to {tex_path}\n")
    print(f"Generated {len(set(romanji))} unique vocabulary entries.")
    print(f"Saved {tex_path} and {pdf_path}")


if __name__ == "__main__":
    main()