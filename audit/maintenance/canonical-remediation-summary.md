# 正本複合語680語・227対話シナリオによる保留候補救済監査レポート (Phase 1〜60 完了記録)

- **対象データセット**: `data/verified_canonical_compounds.json`
- **機械監査レポート**: `audit/maintenance/canonical-compounds-batch1-20261019.json`
- **派生典籍出力**: `docs/Valnes_dialogues.html` / `docs/Valnes_dialogues.pdf` / `docs/VALNES_DIALOGUES_COMPANION.md`
- **検証済み正本複合語数**: **680 語**（全60バッチ：`Batch 1` 〜 `Batch 60`）
- **実証済み2話者対話シナリオ数**: **227 篇**（`CANON-CONV-01` 〜 `CANON-COLAB-60`）
- **監査判定**: **`ZERO_FLAGS_VERIFIED`（監査フラグ 0 件）**
- **旧保留台帳（`data/emergent_lexicon_audit.json`）総数**: 1020 件（うち日常会話 `CONV-*` 500 件）
- **正本複合語へのリマッピング（救済対応付け）完了件数**: **680 件**

## 1. バッチ別構成と監査結果

| バッチ | シナリオ範囲 | 収録語数 | 構成語根の正本自立率 | 2話者対話再利用 | 監査フラグ件数 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Batch 1** | `CANON-CONV-01` 〜 `CANON-CONV-10` | 30 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 2** | `CANON-CONV-11` 〜 `CANON-CONV-12` | 6 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 3** | `CANON-CONV-13` 〜 `CANON-CONV-14` | 6 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 4** | `CANON-CONV-15` 〜 `CANON-CONV-18` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 5** | `CANON-CONV-19` 〜 `CANON-CONV-20` | 6 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 6** | `CANON-CONV-21` 〜 `CANON-CONV-24` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 7** | `CANON-CONV-25` 〜 `CANON-CONV-28` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 8** | `CANON-CONV-29` 〜 `CANON-CONV-32` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 9** | `CANON-CONV-33` 〜 `CANON-CONV-36` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 10** | `CANON-CONV-37` 〜 `CANON-CONV-40` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 11** | `CANON-CONV-41` 〜 `CANON-CONV-44` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 12** | `CANON-CONV-45` 〜 `CANON-CONV-48` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 13** | `CANON-CONV-49` 〜 `CANON-CONV-52` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 14** | `CANON-CONV-53` 〜 `CANON-CONV-56` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 15** | `CANON-CONV-57` 〜 `CANON-CONV-60` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 16** | `CANON-CONV-61` 〜 `CANON-CONV-64` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 17** | `CANON-CONV-65` 〜 `CANON-CONV-68` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 18** | `CANON-CONV-69` 〜 `CANON-CONV-72` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 19** | `CANON-CONV-73` 〜 `CANON-CONV-76` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 20** | `CANON-CONV-77` 〜 `CANON-CONV-80` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 21** | `CANON-CONV-81` 〜 `CANON-CONV-84` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 22** | `CANON-CONV-85` 〜 `CANON-CONV-88` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 23** | `CANON-CONV-89` 〜 `CANON-CONV-92` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 24** | `CANON-CONV-93` 〜 `CANON-CONV-96` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 25** | `CANON-CONV-97` 〜 `CANON-CONV-100` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 26** | `CANON-CONV-101` 〜 `CANON-CONV-104` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 27** | `CANON-CONV-105` 〜 `CANON-CONV-108` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 28** | `CANON-CONV-109` 〜 `CANON-CONV-112` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 29** | `CANON-CONV-113` 〜 `CANON-CONV-116` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 30** | `CANON-CONV-117` 〜 `CANON-CONV-120` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 31** | `CANON-CONV-121` 〜 `CANON-CONV-124` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 32** | `CANON-CONV-125` 〜 `CANON-CONV-128` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 33** | `CANON-CONV-129` 〜 `CANON-CONV-132` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 34** | `CANON-CONV-133` 〜 `CANON-CONV-136` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 35** | `CANON-CONV-137` 〜 `CANON-CONV-140` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 36** | `CANON-CONV-141` 〜 `CANON-CONV-144` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 37** | `CANON-CONV-145` 〜 `CANON-CONV-148` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 38** | `CANON-CONV-149` 〜 `CANON-CONV-152` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 39** | `CANON-CONV-153` 〜 `CANON-CONV-156` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 40** | `CANON-CONV-157` 〜 `CANON-CONV-160` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 41** | `CANON-CONV-161` 〜 `CANON-CONV-164` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 42** | `CANON-CONV-165` 〜 `CANON-CONV-167` | 8 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 43** | `CANON-COLAB-01` 〜 `CANON-COLAB-04` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 44** | `CANON-COLAB-05` 〜 `CANON-COLAB-08` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 45** | `CANON-COLAB-09` 〜 `CANON-COLAB-10` | 6 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 46** | `CANON-COLAB-11` 〜 `CANON-COLAB-13` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 47** | `CANON-COLAB-14` 〜 `CANON-COLAB-16` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 48** | `CANON-COLAB-17` 〜 `CANON-COLAB-20` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 49** | `CANON-COLAB-21` 〜 `CANON-COLAB-23` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 50** | `CANON-COLAB-24` 〜 `CANON-COLAB-26` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 51** | `CANON-COLAB-27` 〜 `CANON-COLAB-30` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 52** | `CANON-COLAB-31` 〜 `CANON-COLAB-33` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 53** | `CANON-COLAB-34` 〜 `CANON-COLAB-36` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 54** | `CANON-COLAB-37` 〜 `CANON-COLAB-40` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 55** | `CANON-COLAB-41` 〜 `CANON-COLAB-43` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 56** | `CANON-COLAB-44` 〜 `CANON-COLAB-46` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 57** | `CANON-COLAB-47` 〜 `CANON-COLAB-50` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 58** | `CANON-COLAB-51` 〜 `CANON-COLAB-53` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 59** | `CANON-COLAB-54` 〜 `CANON-COLAB-56` | 9 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |
| **Batch 60** | `CANON-COLAB-57` 〜 `CANON-COLAB-60` | 12 語 | 100% (`data/lexicon.json`) | 100% 実証済み | **0 件** |

## 2. 旧保留候補（非自立語根を含む合成語）からのリマッピング対応表（抜粋50件＋全680件要約）

旧生成スクリプト（`CORE_MORPHEMES` の非辞書語根 `kel`, `vas`, `pel` 等や `r[:3]` 切り詰めを使用していたもの）で生成された保留候補に対し、正本辞書（`data/lexicon.json`）の単独語根2つのみを連結した正本複合語680語を1対1で対応付けました。

| 正本複合語 ID | 正本複合語 (`nrs`) | 正本語根分解 | 日本語定義 | 代替対象の旧保留 ID | 旧保留語 (`legacyNrs`) | 旧形態素 |
| :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| `#31001` | **`darfalun`** | `dar + falun` | 露光、朝露の煌めき、光る水滴 | `#40521` | `kelvas` | `kel + vas` |
| `#31002` | **`darterin`** | `dar + terin` | 雫茶、澄んだ朝茶、湧き水の煎じ茶 | `#40522` | `kelzen` | `kel + zen` |
| `#31003` | **`havsirin`** | `hav + sirin` | 静かなひととき、安らぎの刻、平穏な時間 | `#40523` | `kelfen` | `kel + fen` |
| `#31004` | **`nerdarel`** | `ner + darel` | 滋養スープ、具だくさんの温汁、栄養煮込み汁 | `#40524` | `tandar` | `tan + dar` |
| `#31005` | **`nervorin`** | `ner + vorin` | 滋養果実、熟した保存果、食卓の木の実 | `#40525` | `tansul` | `tan + sul` |
| `#31006` | **`nerelir`** | `ner + elir` | 食の歓び、団欒の満腹感、食事の幸せ | `#40526` | `tanbion` | `tan + bion` |
| `#31007` | **`veltasel`** | `vel + tasel` | 木の腰掛け椅子、木製スツール、木組みの座席 | `#40527` | `tansir` | `tan + sir` |
| `#31008` | **`velgovan`** | `vel + govan` | 木造の住まい、木の家屋、林間の家 | `#40528` | `tanpar` | `tan + par` |
| `#31009` | **`kymvorn`** | `kym + vorn` | 寝室、夜の私室、休息の間 | `#40529` | `tanvel` | `tan + vel` |
| `#31010` | **`talporan`** | `tal + poran` | 土の歩道、踏み固めた小道、野の散歩道 | `#40530` | `tanvan` | `tan + van` |
| `#31011` | **`alinvelin`** | `alin + velin` | 白花、純白の草花、白い小花 | `#40531` | `tankor` | `tan + kor` |
| `#31012` | **`veltalom`** | `vel + talom` | 木立の広場、並木原、木陰の平地 | `#40532` | `tantas` | `tan + tas` |
| `#31013` | **`velkypal`** | `vel + kypal` | 木箱、木製の小箱、木組みの収納匣 | `#40533` | `tanlin` | `tan + lin` |
| `#31014` | **`hanopamel`** | `hano + pamel` | 今日の手記帳、当日の日誌、本日の控え帳 | `#40534` | `tanlen` | `tan + len` |
| `#31015` | **`vellerel`** | `vel + lerel` | 木の扉、木戸、木組みの戸口 | `#40535` | `tankyr` | `tan + kyr` |
| `#31016` | **`kymcelen`** | `kym + celen` | 夜空、夜の天蓋、闇の蒼穹 | `#40536` | `tanmin` | `tan + min` |
| `#31017` | **`tynivyr`** | `tyni + vyr` | 銀星、白銀の星明かり、銀色に輝く星 | `#40537` | `tanfen` | `tan + fen` |
| `#31018` | **`kymfenor`** | `kym + fenor` | 夜語り、夜のひそやかな語らい、夜更けの話し声 | `#40538` | `mordar` | `mor + dar` |
| `#31019` | **`talzyvas`** | `tal + zyvas` | 大地の生気、土の養生力、自然の健やかさ | `#40539` | `morsul` | `mor + sul` |
| `#31020` | **`darzyvil`** | `dar + zyvil` | 水薬、薬草の雫、煎じ薬液 | `#40540` | `morbion` | `mor + bion` |
| `#31021` | **`kymtymis`** | `kym + tymis` | 夜眠り、深い安眠、夜の熟睡 | `#40541` | `morvas` | `mor + vas` |
| `#31022` | **`hanorenan`** | `hano + renan` | 今日の商い、本日の取引、当日の物々交換 | `#40542` | `morzen` | `mor + zen` |
| `#31023` | **`hanocalun`** | `hano + calun` | 今日の相談、本日の語らい、当日の打ち合わせ | `#40543` | `mormol` | `mor + mol` |
| `#31024` | **`zydsoras`** | `zyd + soras` | 事実記録、実相の記憶、確かな控え | `#40544` | `morkel` | `mor + kel` |
| `#31025` | **`taldaris`** | `tal + daris` | 湧き水、地下水脈、大地の清流 | `#40545` | `mortan` | `mor + tan` |
| `#31026` | **`velwylas`** | `vel + wylas` | 木立のそよ風、樹間を渡る風、木漏れ日の風 | `#40546` | `mormer` | `mor + mer` |
| `#31027` | **`vyrdaron`** | `vyr + daron` | 星を映す湖、星影の水面、星見池 | `#40547` | `morfal` | `mor + fal` |
| `#31028` | **`vyrlaris`** | `vyr + laris` | 星の道しるべ、星見の航路、夜空の導き道 | `#40548` | `morvyr` | `mor + vyr` |
| `#31029` | **`senowelin`** | `seno + welin` | 明日の希望、未来への願い、明日への期待 | `#40549` | `morsol` | `mor + sol` |
| `#31030` | **`klorsylim`** | `klor + sylim` | 心の輪、魂の結びつき、円居の共感 | `#40550` | `morcel` | `mor + cel` |
| `#31031` | **`alinvalis`** | `alin + valis` | 白衣、純白の布衣、白い装束 | `#40551` | `morval` | `mor + val` |
| `#31032` | **`tynivalis`** | `tyni + valis` | 銀衣、白銀の装い、銀糸の衣 | `#40552` | `morhar` | `mor + har` |
| `#31033` | **`velkymel`** | `vel + kymel` | 木の寝台、木組みのベッド、木製寝床 | `#40553` | `morlun` | `mor + lun` |
| `#31034` | **`darlaros`** | `dar + laros` | 水上舟、水路の乗り物、渡し舟 | `#40554` | `morkor` | `mor + kor` |
| `#31035` | **`vyrlarar`** | `vyr + larar` | 星見港、星影の船着き場、夜間停泊所 | `#40555` | `mortas` | `mor + tas` |
| `#31036` | **`hanolaris`** | `hano + laris` | 今日の航路、本日の道筋、当日の巡行路 | `#40556` | `morlin` | `mor + lin` |
| `#31037` | **`zydcynur`** | `zyd + cynur` | 心からの感謝、偽りなき謝意、誠実な返礼 | `#40557` | `morlen` | `mor + len` |
| `#31038` | **`zydcynas`** | `zyd + cynas` | 真の友情、揺るぎない親愛、誠の絆 | `#40558` | `morkyr` | `mor + kyr` |
| `#31039` | **`havsaren`** | `hav + saren` | 微笑みの瞬間、笑顔のひととき、和やかな刻 | `#40559` | `mormin` | `mor + min` |
| `#31040` | **`kymlyren`** | `kym + lyren` | 夜想歌、夜の詩歌、宵の調べ | `#40560` | `morfen` | `mor + fen` |
| `#31041` | **`darlyren`** | `dar + lyren` | 水辺の歌、せせらぎの詩、清流の調べ | `#40561` | `kymsel` | `kym + sel` |
| `#31042` | **`velcival`** | `vel + cival` | 木笛の奏楽、樹間の調べ、木々の合奏 | `#40562` | `kympal` | `kym + pal` |
| `#31043` | **`vyrpamel`** | `vyr + pamel` | 星見帳、天体観測記、星図の冊子 | `#40563` | `kymvas` | `kym + vas` |
| `#31044` | **`tynikirel`** | `tyni + kirel` | 銀筆、白銀の鉄筆、銀軸のペン | `#40564` | `kymzen` | `kym + zen` |
| `#31045` | **`zydmemar`** | `zyd + memar` | 実相の思索、事実の熟考、真理の黙想 | `#40565` | `kymmol` | `kym + mol` |
| `#31046` | **`talvelar`** | `tal + velar` | 大地の庭園、土の菜園、里の緑地 | `#40566` | `kymkel` | `kym + kel` |
| `#31047` | **`darvelas`** | `dar + velas` | 露葉、水滴を宿す若葉、濡れ葉 | `#40567` | `kymtan` | `kym + tan` |
| `#31048` | **`nervoril`** | `ner + voril` | 滋養発酵食、熟成保存糧、発酵滋養食 | `#40568` | `kymmer` | `kym + mer` |
| `#31049` | **`tyniserel`** | `tyni + serel` | 銀の小刀、白銀の刃物、銀細工ナイフ | `#40569` | `kymfal` | `kym + fal` |
| `#31050` | **`veldolar`** | `vel + dolar` | 木工仕事、木彫りの勤労、木材加工 | `#40570` | `kymjyl` | `kym + jyl` |

> 全 680 件の完全なリマッピング対応表は `data/verified_canonical_compounds.json` の `remappingTable` フィールドに収録されています。

## 3. 正本・歴史的監査スナップショットの不変性確認

- `data/lexicon.json`（1,008語）、`data/translation_extensions.json`（372語）、`data/grammar_dictionary.json`（83語）、`data/literary_sourcebook.json`（1,463語）は変更せず、生産環境の不変条件を100%維持しています。
- `data/emergent_lexicon_audit.json`（保留1,020件）および `audit/2026-10-16/`・`audit/maintenance/2026-10-18*` の歴史的証跡ファイルは一切改変していません。
- 本番昇格ゲートウェイ（`tools/canonical_promotion_gateway.py`）は機械的検証（`mechanicallyReady: True`）を通過したうえで、人間の言語評議会トークン（`--council-signoff COUNCIL-APPROVE-...`）が与えられるまで `HOLD_FOR_COUNCIL_SIGNOFF` 状態を厳格に維持します。
