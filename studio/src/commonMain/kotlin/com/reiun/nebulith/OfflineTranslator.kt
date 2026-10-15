package com.reiun.nebulith

enum class TranslationDirection { JAPANESE_TO_NRS, NRS_TO_JAPANESE }
data class TranslationResult(val text: String, val method: String, val issues: List<String> = emptyList()) {
    val complete get() = issues.isEmpty() && text.isNotBlank()
}
data class TranslationFrame(val required: Set<String>,val allowed: Set<String>,val passiveAllowed: Set<String>)

/** Controlled-language translator. Unknown clauses fail as a whole, never become fluent guesses. */
class OfflineTranslator(private val entries: List<Entry>, private val examples: List<Example>,private val frames: Map<Int,TranslationFrame>) {
    private val roots=entries.associateBy { it.nrs }
    private val pronouns=mapOf("私" to "mi", "あなた" to "ti", "彼" to "ri", "彼女" to "ri", "彼／彼女" to "ri")
    private val cases=listOf("el","ia","uo","to","de","ku")
    private val jaParticles=mapOf("が" to "el","は" to "el","を" to "ia","へ" to "to","に" to "to","で" to "uo","と" to "ku","によって" to "de")
    // Japanese 'de' can be location OR instrument. Only explicit reviewed place heads map to uo.
    private val reviewedPlaces=setOf("govan","vyrelar","nerar","celvan")
    private data class Form(val id: Int,val past: Boolean=false,val future: Boolean=false,val progress: Boolean=false,
        val negative: Boolean=false,val voice: Boolean=false,val aspect: String="")
    private val japaneseForms=linkedMapOf<String,Form>()
    private val canonical=linkedMapOf<Form,String>()
    private val jaIndex=entries.flatMap { e->glosses(e).map { it to e } }.groupBy({it.first},{it.second})
    private val adjectives=entries.filter { "形" in it.pos }.flatMap { e->glosses(e).map { it to e } }
    init {
        fun verb(id: Int,base: String,past: String,progress: String,negative: String,negativePast: String,polite: String,politePast: String,politeNegative: String) {
            val variants=listOf(base to Form(id),past to Form(id,past=true),progress to Form(id,progress=true),
                negative to Form(id,negative=true),negativePast to Form(id,past=true,negative=true),
                (base+"だろう") to Form(id,future=true),polite to Form(id),politePast to Form(id,past=true),politeNegative to Form(id,negative=true))
            for((word,form) in variants) { japaneseForms[word]=form; if(form !in canonical) canonical[form]=word }
        }
        verb(16,"輝く","輝いた","輝いている","輝かない","輝かなかった","輝きます","輝きました","輝きません")
        verb(16,"光る","光った","光っている","光らない","光らなかった","光ります","光りました","光りません")
        // Keep the reviewed intransitive canonical sense, not the dictionary's transitive 'illuminate'.
        canonical[Form(16)]="輝く"; canonical[Form(16,past=true)]="輝いた"
        canonical[Form(16,progress=true)]="輝いている";canonical[Form(16,negative=true)]="輝かない"
        canonical[Form(16,past=true,negative=true)]="輝かなかった";canonical[Form(16,future=true)]="輝くだろう"
        verb(902,"歩く","歩いた","歩いている","歩かない","歩かなかった","歩きます","歩きました","歩きません")
        verb(953,"観測する","観測した","観測している","観測しない","観測しなかった","観測します","観測しました","観測しません")
        verb(972,"食べる","食べた","食べている","食べない","食べなかった","食べます","食べました","食べません")
        for((word,form) in listOf("観測される" to Form(953,voice=true),"観測された" to Form(953,past=true,voice=true),
            "観測されない" to Form(953,negative=true,voice=true),"輝き始める" to Form(16,aspect="ast"),
            "歩き始める" to Form(902,aspect="ast"),"食べ始める" to Form(972,aspect="ast"),
            "繰り返し輝く" to Form(16,aspect="cor"),"繰り返し歩く" to Form(902,aspect="cor"),
            "繰り返し観測する" to Form(953,aspect="cor"),"繰り返し食べる" to Form(972,aspect="cor"),
            "である" to Form(906),"です" to Form(906),"だ" to Form(906),"だった" to Form(906,past=true),
            "であった" to Form(906,past=true),"でした" to Form(906,past=true),"ではない" to Form(906,negative=true),
            "ではなかった" to Form(906,past=true,negative=true),"であろう" to Form(906,future=true),"でしょう" to Form(906,future=true))) {
            japaneseForms[word]=form; if(form !in canonical)canonical[form]=word
        }
    }
    private class Unsupported(message: String): Exception(message)
    private fun reject(message: String): Nothing = throw Unsupported(message)
    private fun glosses(e: Entry)=e.meaningJa.split('、','／').map { it.trim() }.filter { it.isNotBlank() }
    private fun label(e: Entry)=glosses(e).first()
    private fun jaKey(s: String)=s.trim().replace(Regex("\\s+"),"").replace('？','?').trimEnd('。','.')
    private fun nrsKey(s: String)=s.trim().lowercase().replace(Regex("\\s+")," ").trimEnd('.')

    fun translate(input: String,direction: TranslationDirection): TranslationResult {
        if(input.isBlank()) return TranslationResult("","入力待ち")
        if(input.length>4000) return TranslationResult("","未対応",listOf("一度に入力できるのは4,000文字までです。"))
        val key=if(direction==TranslationDirection.JAPANESE_TO_NRS) jaKey(input) else nrsKey(input)
        val exact=examples.filter { (if(direction==TranslationDirection.JAPANESE_TO_NRS) jaKey(it.translation) else nrsKey(it.nrs))==key }
        val known=exact.map { if(direction==TranslationDirection.JAPANESE_TO_NRS)it.nrs else it.translation }.distinct()
        if(known.size==1)return TranslationResult(known.single(),"公式例文一致")
        if(known.size>1)return TranslationResult("","要確認",listOf("公式例文の対応が複数あります。入力を具体化してください。"))
        val parts=Regex(if(direction==TranslationDirection.JAPANESE_TO_NRS)"[^。！？.!?]+[。！？.!?]*" else "[^.!?]+[.!?]*").findAll(input).map { it.value.trim() }.filter { it.isNotBlank() }.toList()
        if(parts.isEmpty())return TranslationResult("","未対応",listOf("文章または辞書にある語を入力してください。"))
        val outputs=mutableListOf<String>();val issues=mutableListOf<String>()
        for((i,part) in parts.withIndex()) {
            try {
                if(part.length>240)reject("1文を240文字以内に区切ってください。")
                val match=examples.filter { (if(direction==TranslationDirection.JAPANESE_TO_NRS)jaKey(it.translation) else nrsKey(it.nrs))==(if(direction==TranslationDirection.JAPANESE_TO_NRS)jaKey(part) else nrsKey(part)) }
                    .map { if(direction==TranslationDirection.JAPANESE_TO_NRS)it.nrs else it.translation }.distinct()
                outputs.add(if(match.size==1)match.single() else if(direction==TranslationDirection.JAPANESE_TO_NRS)fromJapanese(part) else fromNrs(part))
            } catch(e: Unsupported) { issues.add("${i+1}文目：${e.message}") }
        }
        return if(issues.isEmpty()) TranslationResult(outputs.joinToString(if(direction==TranslationDirection.JAPANESE_TO_NRS) " " else ""),"辞書・対応文型による変換")
            else TranslationResult("","要確認",issues)
    }

    private fun jaPhrase(s: String,adjectiveAllowed: Boolean=false,depth: Int=0): String {
        if(depth>2)reject("修飾が複雑です。名詞句を短くしてください。")
        val text=s.trim(); if(text.isEmpty())reject("名詞句が空です。")
        pronouns[text]?.let { return it }
        val direct=(jaIndex[text].orEmpty()+if(adjectiveAllowed)jaIndex[text+"な"].orEmpty().filter {"形" in it.pos} else emptyList())
            .distinctBy {it.id}.filter { "名" in it.pos || adjectiveAllowed && "形" in it.pos }
        if(direct.size==1)return direct.single().nrs
        if(direct.size>1)reject("「$text」に複数の候補があります："+direct.take(5).joinToString { "${it.nrs} (#${it.id})" })
        if(text.count { it=='の' }==1) {
            val p=text.split('の');return jaPhrase(p[1],adjectiveAllowed,depth+1)+" en "+jaPhrase(p[0],false,depth+1)
        }
        val modified=mutableSetOf<String>()
        for((g,e) in adjectives.filter { (g,_)->g.length>=2 && text.startsWith(g) && text.length>g.length }) {
            try { modified.add(jaPhrase(text.drop(g.length),false,depth+1)+" "+e.nrs) } catch(_: Unsupported) {}
        }
        if(modified.size==1)return modified.single()
        if(modified.size>1)reject("「$text」の修飾関係を一意に決められません。")
        reject("「$text」は対応する名詞・形容詞を確定できません。辞書の日本語語義を使ってください。")
    }
    private fun nrsPhrase(words: List<String>,adjectiveAllowed: Boolean=false,depth: Int=0): String {
        if(words.isEmpty() || depth>2)reject("名詞句が空、または修飾が複雑です。")
        if(words.count { it=="en" }>1)reject("属格enの入れ子は未対応です。")
        if("en" in words) {
            val at=words.indexOf("en")
            return nrsPhrase(words.drop(at+1),false,depth+1)+"の"+nrsPhrase(words.take(at),adjectiveAllowed,depth+1)
        }
        val head=when(words.first()) { "mi"->"私";"ti","taas"->"あなた";"ri"->"彼／彼女";else->{
            val e=roots[words.first()] ?: reject("未知語「${words.first()}」。原文を確認してください。")
            if("名" !in e.pos && !(adjectiveAllowed && "形" in e.pos))reject("「${e.nrs}」を名詞句として解釈できません。")
            label(e)
        } }
        return words.drop(1).joinToString("") { token ->
            val e=roots[token] ?: reject("未知の修飾語「$token」。")
            if("形" !in e.pos)reject("後置修飾語「$token」は対応する形容詞ではありません。")
            label(e)
        }+head
    }
    private fun validate(form: Form,args: Map<String,String>) {
        val frame=frames[form.id] ?: reject("未対応の動詞です。")
        val allowed=if(form.voice)frame.passiveAllowed else frame.allowed
        if(!args.keys.containsAll(frame.required))reject("主語、またはコピュラの補語が必要です。")
        if(args.keys.any { it !in allowed })reject("動詞の項構造に合わない格が含まれます。")
        if(form !in canonical)reject("この時制・相・否定・態の組み合わせは初版の対応範囲外です。")
    }
    private fun fromJapanese(part: String): String {
        var text=jaKey(part);var question=text.endsWith('?');text=text.trimEnd('?')
        if(text.endsWith("か")) { question=true;text=text.dropLast(1) }
        // A single dictionary term is useful, but is never expanded into a guessed sentence.
        if(!question)try { return jaPhrase(text) }catch(_: Unsupported) {}
        val candidates=mutableListOf<Pair<Form,Map<String,String>>>()
        var lastProblem="対応文型を使ってください（例：私は家へ歩く。／私は星を観測する。）。"
        for((ending,form) in japaneseForms.entries.sortedByDescending { it.key.length }) {
            if(!text.endsWith(ending))continue
            val body=text.dropLast(ending.length)
            try {
                val args=if(form.id==906) {
                    val positions=body.indices.filter { body[it]=='は' || body[it]=='が' }
                    val valid=positions.mapNotNull { at -> try { mapOf("el" to jaPhrase(body.take(at)),"ia" to jaPhrase(body.drop(at+1),true)) } catch(_: Unsupported) { null } }
                    if(valid.distinct().size!=1)reject("AはBである、のAとBを確定できません。")
                    valid.distinct().single()
                } else parseJapaneseArguments(body)
                validate(form,args); candidates.add(form to args)
            }catch(e: Unsupported) {lastProblem=e.message ?: lastProblem}
        }
        val distinct=candidates.distinct()
        if(distinct.size>1)reject("文の解釈が複数あります。主語・目的語・場所を具体化してください。")
        if(distinct.isEmpty())reject(lastProblem)
        val(form,args)=distinct.single()
        val root=entries.single { it.id==form.id }.nrs
        val tokens=mutableListOf<String>()
        if(form.past)tokens.add("fe");if(form.future)tokens.add("se");if(form.progress)tokens.add("di");if(form.negative)tokens.add("ne")
        tokens.add((if(form.voice)"re" else "")+root+form.aspect)
        for(case in cases)args[case]?.let {tokens.add(case);tokens.add(it)}
        if(question)tokens.add("ka")
        val result=tokens.joinToString(" ")
        return result.replaceFirstChar { it.uppercase() }+if(question)"?" else "."
    }
    private fun parseJapaneseArguments(text: String): Map<String,String> {
        val possibilities=mutableListOf<Map<String,String>>()
        var budget=500
        fun parse(rest: String,args: Map<String,String>) {
            if(possibilities.size>10)return
            if(rest.isEmpty()) { possibilities.add(args);return }
            for((particle,case) in jaParticles) {
                if(case in args)continue
                var from=0
                while(true) {
                    if(--budget<0)reject("助詞の解釈候補が多すぎます。名詞句を短くしてください。")
                    val at=rest.indexOf(particle,from);if(at<0)break;from=at+particle.length
                    try {
                        val phrase=jaPhrase(rest.take(at))
                        if(case=="uo" && phrase.substringBefore(' ') !in reviewedPlaces)
                            reject("助詞「で」の場所・道具の解釈を確定できません。初版の場所は家・天文台・食堂・天球です。")
                        parse(rest.drop(at+particle.length),args+(case to phrase))
                    }catch(_: Unsupported) {}
                }
            }
        }
        parse(text,emptyMap())
        val distinct=possibilities.distinct()
        if(distinct.size!=1)reject("主語・目的語・場所の語義か助詞を確定できません。省略せず「私が星を観測する」のように入力してください。")
        return distinct.single()
    }
    private fun fromNrs(part: String): String {
        if(Regex("[^a-zA-Z'\\s.!?]").containsMatchIn(part))reject("NRSには半角英字・空白・対応する句読点を使ってください。")
        val punctuationQuestion=part.trim().endsWith('?')
        val tokens=part.trim().trimEnd('.','!','?').lowercase().split(Regex("\\s+")).toMutableList()
        if(tokens.size==1 && !punctuationQuestion)return nrsPhrase(tokens)
        val question=tokens.lastOrNull()=="ka";if(question)tokens.removeAt(tokens.lastIndex)
        if(punctuationQuestion && !question)reject("疑問文は文末kaを明示してください。")
        val prefixes=mutableSetOf<String>()
        while(tokens.firstOrNull() in listOf("fe","se","di","ne")) {
            val prefix=tokens.removeAt(0);if(!prefixes.add(prefix))reject("前置小詞が重複しています。")
        }
        if("fe" in prefixes && "se" in prefixes)reject("過去feと未来seを同時に指定できません。")
        var predicate=tokens.firstOrNull() ?: reject("動詞がありません。")
        tokens.removeAt(0)
        val voice=predicate.startsWith("re") && predicate !in frames.keys.mapNotNull { id->entries.find {it.id==id}?.nrs }
        if(voice)predicate=predicate.drop(2)
        var aspect=""
        if(predicate.endsWith("ast") || predicate.endsWith("cor")) { aspect=predicate.takeLast(3);predicate=predicate.dropLast(3) }
        val entry=roots[predicate] ?: reject("未対応または未知の動詞「$predicate」。")
        val form=Form(entry.id,"fe" in prefixes,"se" in prefixes,"di" in prefixes,"ne" in prefixes,voice,aspect)
        val grouped=linkedMapOf<String,MutableList<String>>();var current:String?=null
        for(token in tokens) {
            if(token in cases) { if(token in grouped)reject("格標識「$token」が重複しています。");current=token;grouped[token]=mutableListOf() }
            else { val c=current ?: reject("格標識のない語「$token」。");grouped.getValue(c).add(token) }
        }
        val args=grouped.mapValues { (case,words)->nrsPhrase(words,entry.id==906 && case=="ia") }
        validate(form,args)
        val adjectiveComplement=entry.id==906 && grouped["ia"]?.firstOrNull()?.let { roots[it]?.pos?.contains("形") }==true
        var complement=args["ia"].orEmpty()
        var verb=canonical.getValue(form)
        if(adjectiveComplement) {
            if(complement.endsWith("い") && complement !in setOf("きれい","嫌い")) {
                val stem=complement.dropLast(1)
                complement=when { form.past && form.negative->stem+"くなかったです";form.negative->stem+"くないです"
                    form.past->stem+"かったです";form.future->complement+"でしょう";else->complement+"です" }
                verb=""
            } else complement=complement.removeSuffix("な")
        }
        val sentence=buildString {
            append(args.getValue("el"));append("は")
            for((case,particle) in listOf("uo" to "で","to" to "へ","de" to "によって","ku" to "と","ia" to if(entry.id==906)"" else "を"))
                args[case]?.let { append(if(case=="ia" && adjectiveComplement)complement else it);append(particle) }
            append(verb);if(question)append("か");append("。")
        }
        return sentence
    }
}
