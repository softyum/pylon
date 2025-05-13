def detect_garbled_ratio(text):
    total_chars = len(text)
    if total_chars == 0:
        return 0.0

    garbled_count = 0

    for char in text:
        # 如果字符不可打印，认为是乱码
        if not char.isprintable():
            garbled_count += 1
        # 或者加入更严格的判断：不在中文常用范围内也视为乱码
        elif not ('\u4e00' <= char <= '\u9fff' or  # 汉字
                  '\u3400' <= char <= '\u4dbf' or  # 扩展A
                  'a' <= char.lower() <= 'z' or   # 英文字母
                  char in '0123456789。，、；：？！“”‘’（）《》【】—…') :  # 常见标点
            garbled_count += 1

    garbled_ratio = garbled_count / total_chars
    return garbled_ratio

# 示例文本
text = "1ѹ㘩ᄥ䄑䃦᪳ڔ䲎䉋䉏⮰䕆ԍ҈㔱Ƞ䕆 ԍ҈㔱Ꮐ౔េ⽫ᬢ⶚჆喏ຮ౔Ბ⽫͙᱖➥ './../ᴳᬺ喏݅㻲じ̬ ҈㔱ͦ䕆ԍ҈㔱Ƞじ̬҈㔱̺䕆ԍ҈㔱̹᭛स̬Ϧᬢ喏౔ 䃦᪳仂䶡㙆∔䕆ԍ҈㔱໿हȟࢁѹࣶ䗚ᩫ㑂ⴭȠ҈㔱͙ຮ ᰵโㅹ҈㔱喏Ꮐ䭰᱘ϦϞ぀オहसᘻ౔᱘ܶࣽ㶔⮰ܩТȠ 䯲ѿ㒞ह⮰䃦᪳κ᪳䷄̷݃㒞हࢁѹ喏κ᪳᱗݃᪠⤲㔱໿ हȠ䯲ѿ㒞ह⮰᪳「ᓱ䶧ᄲᄥ䄑᪳䉋䉏⮰ڟ䩚Ϧ➕݃ͦ䕆 ԍ҈㔱Ƞ䕆ԍ҈㔱ख݃1ѹ喏⩝េ⽫㔱۟჆Ƞ θȟᔃ"

ratio = detect_garbled_ratio(text)
print(f"乱码占比: {ratio * 100:.2f}%")


text = "主要从事国内外医药政策与法规研究及药物经济学评价研究。E-maih joo蠢；；盎L ，，，≥一t垒霞黧§ei～{ j&：～ 耋0(≥‘≮i钉’、■ cyl990@163．tom 叠 羹一ki盎"

ratio = detect_garbled_ratio(text)
print(f"乱码占比: {ratio * 100:.2f}%")

