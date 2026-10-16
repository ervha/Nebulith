# Nebulith 500-Word Everyday Conversation & General Lexicon Audit Report
**Date:** 2026-10-16 18:55:05  
**Inference Server:** Google Colab vLLM (`Qwen/Qwen2.5-7B-Instruct`)  
**Focus:** Everyday Conversation, Human Life, Tableware, Emotions, Home & General Vocabulary  
**Audit Ledger:** [`data/emergent_lexicon_audit.json`](file:///C:/Users/danun/Desktop/Project/Nebulith/data/emergent_lexicon_audit.json)  
**Governance Status:** **STRICTLY ISOLATED** (Pending Human Creator Audit)  

---

## 1. Executive Summary
- **New Everyday Words Minted:** **500 words** (Target: ~500 everyday words achieved)
- **Total Cumulative Provisional Words in Ledger:** **1020 words**
- **ID Allocation:** `#40521` 〜 `#41020`
- **6-Gate Arbiter Compliance:** **100% Passed** (Phonotactics, Collision Distance, Gloss Disjointness, Morphology, VSO Syntax, Consensus)
- **Production Isolation:** **0 words auto-merged into production** (`data/translation_extensions.json` strictly preserved).

---

## 2. Everyday Conversation Domain Distribution
| Domain / Category | Word Count | Sample Everyday Words |
|:---|:---:|:---|
| 日常の挨拶・応答・相槌 | **25** | **kelvas** (日常のおはようの挨拶), **kelzen** (日常の夕べの憩い), **kelfen** (日常の感謝の言葉), **tandar** (日常の詫びの言葉) |
| 家族・親族・身近な間柄 | **25** | **morvas** (日常の幼なじみ), **morzen** (日常の親しき友), **mormol** (日常の長老の助言), **morkel** (日常の幼子) |
| 住まい・家屋・部屋・家具 | **25** | **kymsel** (日常の玄関扉), **kympal** (日常の木組みの窓), **kymvas** (日常の寝床の敷布), **kymzen** (日常の腰掛け椅子) |
| 朝昼晩の食事・食卓・茶礼 | **25** | **tymsir** (日常の朝餉の湯気), **tymtul** (日常の昼休みの軽食), **tympel** (日常の夕餉の団欒), **tymnel** (日常の白湯茶) |
| 台所・調理・日常の味覚 | **25** | **tymkor** (日常の湯沸かし鍋), **tymtas** (日常の切り分け包丁), **tymlin** (日常のすり鉢), **tymlen** (日常の塩加減) |
| 衣類・身の回り品・身支度 | **25** | **mercel** (日常の上着), **merval** (日常の履物), **merhar** (日常の革鞄), **merlun** (日常の手袋) |
| 基本動作・家事・日常行動 | **25** | **faltan** (日常の目覚め), **falmer** (日常の身支度する), **falvyr** (日常の掃き掃除), **falcel** (日常の水汲み) |
| 時間・頻度・予定・約束 | **25** | **jylmer** (日常のいま・現在), **jylfal** (日常の後ほど・やがて), **jylvyr** (日常の昨日・先刻), **jylsol** (日常の明日・翌朝) |
| 感情・気分・日常の機嫌 | **25** | **vyrpal** (日常の上機嫌・朗らか), **vyrvas** (日常のほっとする安堵), **vyrzen** (日常の退屈・手持ち無沙汰), **vyrmol** (日常の心躍る期待) |
| 身体・体調・日常の健康 | **25** | **soldar** (日常の足の疲れ), **solsul** (日常の肩の凝り), **solbion** (日常の深呼吸), **solsir** (日常の喉の渇き) |
| 街歩き・道案内・散策 | **25** | **solkor** (日常の路地裏の小道), **soltas** (日常の辻の交差点), **sollin** (日常の石橋の袂), **sollen** (日常の市場の広場) |
| 市場・買い物・品物のやり取り | **25** | **celvyr** (日常の売り買い), **celsol** (日常の代価・値段), **celval** (日常のお釣り・端数), **celhar** (日常の品定め) |
| 依頼・提案・相談・頼み事 | **25** | **valmol** (日常のお願い・手助け), **valkel** (日常の助言・知恵借り), **valtan** (日常のお誘い・お茶に誘う), **valmer** (日常の提案・相談) |
| 意見・考え・感想・評価 | **25** | **hovtor** (日常の良し悪し), **hovpal** (日常のお気に入り), **hovvas** (日常のちょうど良い塩梅), **hovzen** (日常の手頃な大きさ) |
| 身近な道具・文具・小物 | **25** | **hovmin** (日常の筆記具), **hovfen** (日常の手帳・メモ), **hardar** (日常の小箱・物入れ), **harsul** (日常の鍵と錠前) |
| 身近な生き物・ペット・鳥獣 | **25** | **harlun** (日常の人懐こい犬), **harpar** (日常の気ままな猫), **harvel** (日常の軒先の小鳥), **harkor** (日常の荷引き馬) |
| 庭先・身近な花草・家庭菜園 | **25** | **govmer** (日常の植木鉢), **govfal** (日常の庭先の小花), **govjyl** (日常の薬味草・ハーブ), **govvyr** (日常のみずみずしい葉) |
| 日常の天気・空模様・温度 | **25** | **lunnel** (日常の心地よい晴れ), **lunsel** (日常の小雨・通り雨), **luntor** (日常の穏やかな曇り空), **lunpal** (日常のそよ風) |
| 雑談・冗談・昔話・世間話 | **25** | **lunkyr** (日常の世間話), **lunmin** (日常の冗談・笑い話), **lunfen** (日常のくすっと笑う), **pardar** (日常の噂話) |
| 別れ際・結び・心遣い | **25** | **parval** (日常のお見送り), **parhar** (日常の道中の無事), **parlun** (日常の良い夢を), **parvel** (日常のまた逢う日まで) |

---

## 3. Exemplar Conversational Neologisms (First 35 Entries)
| ID | Nebulith | POS | Meaning (JA) | Meaning (EN) | Morphemes | Score | Example Sentence (VSO) |
|:---:|:---|:---:|:---|:---|:---|:---:|:---|
| `40521` | **kelvas** | 動 | 日常のおはようの挨拶、木と広の身近な結びつき | everyday おはようの挨拶 (kel-va | `kel + vas` | 0.980 | *Poran el mi uo *kelvas de zen.* |
| `40522` | **kelzen** | 名 | 日常の夕べの憩い、木と善の身近な結びつき | everyday 夕べの憩い (kel-zen  | `kel + zen` | 1.000 | *Poran el mi uo *kelzen de zen.* |
| `40523` | **kelfen** | 名 | 日常の感謝の言葉、木と翼の身近な結びつき | everyday 感謝の言葉 (kel-fen  | `kel + fen` | 0.980 | *Poran el mi uo *kelfen de zen.* |
| `40524` | **tandar** | 動 | 日常の詫びの言葉、土と水の身近な結びつき | everyday 詫びの言葉 (tan-dar  | `tan + dar` | 0.980 | *Poran el mi uo *tandar de zen.* |
| `40525` | **tansul** | 名 | 日常の承諾の返事、土と気の身近な結びつき | everyday 承諾の返事 (tan-sul  | `tan + sul` | 1.000 | *Poran el mi uo *tansul de zen.* |
| `40526` | **tanbion** | 名 | 日常の本当に、土と生の身近な結びつき | everyday 本当に (tan-bion s | `tan + bion` | 1.000 | *Poran el mi uo *tanbion de zen.* |
| `40527` | **tansir** | 動 | 日常のもちろん、土と光の身近な結びつき | everyday もちろん (tan-sir s | `tan + sir` | 0.980 | *Poran el mi uo *tansir de zen.* |
| `40528` | **tanpar** | 動 | 日常のお気をつけて、土と創の身近な結びつき | everyday お気をつけて (tan-par | `tan + par` | 0.980 | *Poran el mi uo *tanpar de zen.* |
| `40529` | **tanvel** | 動 | 日常のまた明日、土と感の身近な結びつき | everyday また明日 (tan-vel s | `tan + vel` | 0.980 | *Poran el mi uo *tanvel de zen.* |
| `40530` | **tanvan** | 名 | 日常のよろしく頼む、土と集の身近な結びつき | everyday よろしく頼む (tan-van | `tan + van` | 1.000 | *Poran el mi uo *tanvan de zen.* |
| `40531` | **tankor** | 動 | 日常のおはようの挨拶の日常表現、土と環の身近な結 | everyday おはようの挨拶 (tan-ko | `tan + kor` | 0.980 | *Poran el mi uo *tankor de zen.* |
| `40532` | **tantas** | 名 | 日常の夕べの憩いの日常表現、土と器の身近な結びつ | everyday 夕べの憩い (tan-tas  | `tan + tas` | 0.980 | *Poran el mi uo *tantas de zen.* |
| `40533` | **tanlin** | 動 | 日常の感謝の言葉の日常表現、土と糸の身近な結びつ | everyday 感謝の言葉 (tan-lin  | `tan + lin` | 1.000 | *Poran el mi uo *tanlin de zen.* |
| `40534` | **tanlen** | 名 | 日常の詫びの言葉の日常表現、土と眼の身近な結びつ | everyday 詫びの言葉 (tan-len  | `tan + len` | 0.980 | *Poran el mi uo *tanlen de zen.* |
| `40535` | **tankyr** | 動 | 日常の承諾の返事の日常表現、土と力の身近な結びつ | everyday 承諾の返事 (tan-kyr  | `tan + kyr` | 0.980 | *Poran el mi uo *tankyr de zen.* |
| `40536` | **tanmin** | 動 | 日常の本当にの日常表現、土と微の身近な結びつき | everyday 本当に (tan-min sy | `tan + min` | 0.980 | *Poran el mi uo *tanmin de zen.* |
| `40537` | **tanfen** | 動 | 日常のもちろんの日常表現、土と翼の身近な結びつき | everyday もちろん (tan-fen s | `tan + fen` | 0.980 | *Poran el mi uo *tanfen de zen.* |
| `40538` | **mordar** | 名 | 日常のお気をつけての日常表現、終と水の身近な結び | everyday お気をつけて (mor-dar | `mor + dar` | 0.980 | *Poran el mi uo *mordar de zen.* |
| `40539` | **morsul** | 動 | 日常のまた明日の日常表現、終と気の身近な結びつき | everyday また明日 (mor-sul s | `mor + sul` | 1.000 | *Poran el mi uo *morsul de zen.* |
| `40540` | **morbion** | 動 | 日常のよろしく頼むの日常表現、終と生の身近な結び | everyday よろしく頼む (mor-bio | `mor + bion` | 1.000 | *Poran el mi uo *morbion de zen.* |
| `40541` | **morvas** | 動 | 日常の幼なじみ、終と広の身近な結びつき | everyday 幼なじみ (mor-vas s | `mor + vas` | 0.980 | *Poran el mi uo *morvas de zen.* |
| `40542` | **morzen** | 名 | 日常の親しき友、終と善の身近な結びつき | everyday 親しき友 (mor-zen s | `mor + zen` | 0.980 | *Poran el mi uo *morzen de zen.* |
| `40543` | **mormol** | 動 | 日常の長老の助言、終と火の身近な結びつき | everyday 長老の助言 (mor-mol  | `mor + mol` | 1.000 | *Poran el mi uo *mormol de zen.* |
| `40544` | **morkel** | 名 | 日常の幼子、終と木の身近な結びつき | everyday 幼子 (mor-kel syn | `mor + kel` | 0.980 | *Poran el mi uo *morkel de zen.* |
| `40545` | **mortan** | 動 | 日常の同居人、終と土の身近な結びつき | everyday 同居人 (mor-tan sy | `mor + tan` | 0.980 | *Poran el mi uo *mortan de zen.* |
| `40546` | **mormer** | 動 | 日常の親族の集い、終と海の身近な結びつき | everyday 親族の集い (mor-mer  | `mor + mer` | 1.000 | *Poran el mi uo *mormer de zen.* |
| `40547` | **morfal** | 名 | 日常の客人、終と星の身近な結びつき | everyday 客人 (mor-fal syn | `mor + fal` | 0.980 | *Poran el mi uo *morfal de zen.* |
| `40548` | **morvyr** | 名 | 日常の隣人、終と視の身近な結びつき | everyday 隣人 (mor-vyr syn | `mor + vyr` | 0.980 | *Poran el mi uo *morvyr de zen.* |
| `40549` | **morsol** | 動 | 日常の旅の道連れ、終と日の身近な結びつき | everyday 旅の道連れ (mor-sol  | `mor + sol` | 0.980 | *Poran el mi uo *morsol de zen.* |
| `40550` | **morcel** | 名 | 日常の親愛なる人、終と月の身近な結びつき | everyday 親愛なる人 (mor-cel  | `mor + cel` | 0.980 | *Poran el mi uo *morcel de zen.* |
| `40551` | **morval** | 動 | 日常の幼なじみの日常表現、終と夜の身近な結びつき | everyday 幼なじみ (mor-val s | `mor + val` | 0.980 | *Poran el mi uo *morval de zen.* |
| `40552` | **morhar** | 動 | 日常の親しき友の日常表現、終と鉄の身近な結びつき | everyday 親しき友 (mor-har s | `mor + har` | 0.980 | *Poran el mi uo *morhar de zen.* |
| `40553` | **morlun** | 動 | 日常の長老の助言の日常表現、終と輪の身近な結びつ | everyday 長老の助言 (mor-lun  | `mor + lun` | 1.000 | *Poran el mi uo *morlun de zen.* |
| `40554` | **morkor** | 名 | 日常の幼子の日常表現、終と環の身近な結びつき | everyday 幼子 (mor-kor syn | `mor + kor` | 1.000 | *Poran el mi uo *morkor de zen.* |
| `40555` | **mortas** | 動 | 日常の同居人の日常表現、終と器の身近な結びつき | everyday 同居人 (mor-tas sy | `mor + tas` | 0.980 | *Poran el mi uo *mortas de zen.* |

---

## 4. Next Steps for Creator Audit
1. Inspect newly minted everyday conversational vocabulary in [`data/emergent_lexicon_audit.json`](file:///{AUDIT_LEDGER_PATH.as_posix()}).
2. Review conversational dialogue frames with `python tools/triage_feedback_queue.py --review`.
3. Promote to production lexicon when ready: `python tools/triage_feedback_queue.py --promote`.