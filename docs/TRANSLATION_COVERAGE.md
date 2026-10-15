# 日本語→Nebulithの変換範囲

既存の正本文型を維持し、追加の項構造・活用・形容詞叙述をアプリ用の未監査案として実装しています。一般自由文翻訳の完成を意味しません。

- 対応述語：150。生産的活用の日本語見出し：148。
- 動詞の表層形：2866、形容詞の表層形：426、明示した場所語：20。
- 主語・対象・所有・修飾・授受・起点・場所・道具・共同者を辞書から組み合わせます。
- 五段・一段・サ変・来るの現在／過去／否定／丁寧／進行／始動。希望は検出しても出力規則未定義のため確定しません。
- 形容詞だけの叙述にNebulithのコピュラを補い、語義が複数なら選択後に確定します。
- 英語入力・Nebulithからの逆変換は登録対訳中心で、この対応数には含めません。

## 生産的活用の見出し

| 日本語 | NRS | 辞書ID |
| --- | --- | ---: |
| 輝く | falun | 16 |
| 消滅する | kylen | 21 |
| 航路変更する | larven | 36 |
| 点火する | voran | 58 |
| 煌めく | vyris | 68 |
| 出力する | folin | 129 |
| 記述する | kiran | 136 |
| 配備する | kirpan | 138 |
| シリアライズする | kivkas | 142 |
| クラッシュする | krotpan | 150 |
| 暗号化する | kyvren | 151 |
| 同期する | livpan | 154 |
| 計算する | suf | 166 |
| ルーティングする | tolpan | 179 |
| 入力する | torin | 182 |
| 照会する | velis | 185 |
| インデックスする | veltok | 186 |
| ループする | voret | 187 |
| 送る | wesan | 190 |
| 構文解析する | zevkas | 193 |
| 検証する | zydot | 194 |
| 療養する | darisan | 195 |
| 処方する | darispan | 199 |
| 眠る | tymis | 222 |
| 麻痺する | morpan | 229 |
| 目覚める | revir | 237 |
| 蘇生する | revpan | 239 |
| 鎮静させる | serpanan | 252 |
| 癒す | zyvan | 265 |
| 生きる | zyvel | 267 |
| 呼吸する | zyvelan | 268 |
| 再活性化する | zyvrev | 272 |
| 崩落する | talpan | 298 |
| 氾濫する | darpanan | 341 |
| そよぐ | wylas | 365 |
| 凪ぐ | wylpan | 369 |
| 耕す | talkan | 379 |
| 播種する | teirpan | 388 |
| 結実する | teirpanan | 389 |
| 咲く | velin | 398 |
| 開花する | velpanan | 405 |
| 収穫する | vorken | 424 |
| 吠える | ferpanan | 436 |
| 冬眠する | fervolan | 439 |
| 羽ばたく | volpan | 460 |
| 働く | dolar | 481 |
| 可決する | senpan | 514 |
| 宣告する | turdornan | 527 |
| 布告する | turpanan | 530 |
| 鍛造する | dolaran | 542 |
| 鋳造する | dolpanan | 548 |
| 織る | jylpan | 555 |
| 直す | kirasen | 558 |
| 修理する | kirasen | 558 |
| 切断する | kortan | 559 |
| 取引する | marpan | 569 |
| 投資する | marpanan | 570 |
| 受け取る | martan | 576 |
| 交易する | renan | 582 |
| 焼き入れする | talpyr | 586 |
| 建てる | dompanan | 599 |
| 築く | durpanan | 609 |
| 暮らす | taran | 628 |
| 清書する | kirelpan | 644 |
| 着替える | valson | 678 |
| 作曲する | civpanan | 687 |
| 愛する | cynel | 695 |
| 彩る | falpanan | 702 |
| 信じる | fevas | 705 |
| 忘れる | kores | 712 |
| 思索する | memar | 721 |
| 決断する | minpan | 726 |
| 祈る | minpanan | 727 |
| 尊ぶ | novis | 732 |
| 慰める | sarpanan | 736 |
| 幻視する | muran | 743 |
| 問う | tyras | 753 |
| 語り合う | calun | 840 |
| 見上げる | celan | 841 |
| 覆う | celvor | 844 |
| 歌う | cival | 845 |
| 注ぐ | darlit | 846 |
| 波打つ | darvol | 847 |
| 潜水する | darzanv | 848 |
| 泣く | dyren | 850 |
| 弾ける | falk | 856 |
| 照らす | falvan | 857 |
| 告げる | fenkas | 858 |
| 話す | fenor | 860 |
| ささやく | fensir | 861 |
| 聴く | harvan | 866 |
| 結ぶ | jylas | 873 |
| 編み上げる | jylvor | 874 |
| 書く | kiras | 875 |
| 遮断する | klomas | 876 |
| 閉じる | klovan | 877 |
| 封印する | klovanis | 878 |
| 走る | kupan | 879 |
| しゃがむ | kympan | 885 |
| 凍る | kyrpan | 886 |
| 隠す | kyvel | 887 |
| 迂回する | larvor | 888 |
| 開く | leras | 889 |
| 刻む | nerpan | 893 |
| 登る | novas | 894 |
| 歩く | poran | 902 |
| 行進する | porcon | 903 |
| 通り抜ける | porzan | 904 |
| 燃える | pyran | 905 |
| 笑う | saren | 907 |
| 贈る | zelvan | 909 |
| 協力する | zelvcor | 910 |
| 洗う | serdar | 911 |
| 離す | zelvfas | 912 |
| 触れる | zelvin | 913 |
| 撫でる | serlit | 914 |
| 掴む | serpan | 915 |
| 引っ張る | zelvzan | 916 |
| 書き留める | soran | 919 |
| 踊る | spilan | 921 |
| 探す | syndir | 922 |
| 置く | talsit | 925 |
| 掘る | talvok | 926 |
| 着陸する | talzon | 927 |
| 待つ | taris | 928 |
| 来る | toren | 930 |
| 降りる | tulpan | 935 |
| 繁茂する | velkan | 944 |
| 飛ぶ | veiran | 945 |
| 滑空する | volkin | 946 |
| 跳ぶ | volpas | 947 |
| ダイブする | volzan | 948 |
| 守る | vymin | 951 |
| 観測する | vyrel | 953 |
| 放つ | wylkan | 954 |
| 吹き飛ばす | wylpur | 955 |
| 深呼吸する | wylrev | 956 |
| 泳ぐ | zylan | 958 |
| 飲む | bion | 959 |
| 乾杯する | bionpan | 965 |
| 溶かす | darpan | 969 |
| 食べる | neran | 972 |
| 発酵させる | nerpanv | 987 |
| 煮る | nerpas | 989 |
| 焼く | pyrtos | 1001 |
| 思い出す | sorvel | 30006 |
| 展望する | valcyn | 30007 |
| 予見する | vyrcen | 30008 |

## 辞書にはあるが生成変換が未整備の動詞

語義や活用を推測して自動採用せず、次の拡充対象として残します。

| ID | NRS | 語義 | 未対応理由 |
| ---: | --- | --- | --- |

生成：`node tools/report_translation_coverage.js`。元データは `data/translation_patterns.json` とWeb翻訳エンジンです。
