package com.reiun.nebulith

/** Semantic fixtures plus rejection cases; executed in the shipped JAR/EXE self-test. */
fun checkOfflineTranslation() {
    val engine=OfflineTranslator(Bundle.entries,Bundle.examples,Bundle.translationFrames)
    val ja=TranslationDirection.JAPANESE_TO_NRS;val nrs=TranslationDirection.NRS_TO_JAPANESE
    var passed=0
    fun expect(input: String,direction: TranslationDirection,expected: String) {
        val actual=engine.translate(input,direction)
        check(actual.complete && actual.text==expected) { "Translation mismatch: $input -> $actual; expected $expected" }
        passed++
    }
    fun reject(input: String,direction: TranslationDirection) {
        val actual=engine.translate(input,direction)
        check(!actual.complete && actual.text.isEmpty() && actual.issues.isNotEmpty()) { "Must reject unsupported text: $input -> $actual" }
        passed++
    }
    for(example in Bundle.examples) {
        expect(example.translation,ja,example.nrs);expect(example.nrs,nrs,example.translation)
    }
    expect("私は赤い星を観測します。",ja,"Vyrel el mi ia vyr pyrin.")
    expect("Vyrel el mi ia vyr pyrin.",nrs,"私は赤い星を観測する。")
    expect("私は新しい木を観測しない。",ja,"Ne vyrel el mi ia vel syvan.")
    expect("Ne vyrel el mi ia vel syvan.",nrs,"私は新しい木を観測しない。")
    expect("私はあなたの家へ歩く。",ja,"Poran el mi to govan en ti.")
    expect("Poran el mi to govan en ti.",nrs,"私はあなたの家へ歩く。")
    expect("水は冷たいです。",ja,"Relen el daris ia kyrani.")
    expect("Relen el daris ia kyrani.",nrs,"水は冷たいです。")
    expect("私は星を観測しなかった。",ja,"Fe ne vyrel el mi ia vyr.")
    expect("Fe ne vyrel el mi ia vyr.",nrs,"私は星を観測しなかった。")
    expect("私は星を観測しますか？",ja,"Vyrel el mi ia vyr ka?")
    expect("Vyrel el mi ia vyr ka?",nrs,"私は星を観測するか。")
    expect("私は家で食べます。",ja,"Neran el mi uo govan.")
    expect("Neran el mi uo govan.",nrs,"私は家で食べる。")
    expect("私は歩いた。水は冷たいです。",ja,"Fe poran el mi. Relen el daris ia kyrani.")
    reject("私はテスト未知語を観測する。",ja)
    reject("私は家を歩く。",ja)
    reject("私は家へ食べる。",ja)
    reject("私は望遠鏡で星を観測する。",ja)
    reject("歩く。",ja)
    reject("私は星を観測したので家へ歩いた。",ja)
    reject("私は家へ歩く。続く文は未対応のはず。",ja)
    reject("Falun el vyr?",nrs)
    reject("Fe se falun el vyr.",nrs)
    reject("Falun el vyr ia daris.",nrs)
    reject("Neran el mi to govan.",nrs)
    reject("Vyrel el mi ia nonexistent.",nrs)
    reject("Falun el vyr. Unknown el mi.",nrs)
    reject("a".repeat(4001),nrs)
    val ambiguous=OfflineTranslator(Bundle.entries+Bundle.entries.single { it.id==62 }.copy(id=1200,nrs="teststar"),Bundle.examples,Bundle.translationFrames)
    check(!ambiguous.translate("私は星を観測します。",ja).complete);passed++
    check(engine.translate("",ja).text.isEmpty());passed++
    // UI stale-result prevention and direction swap must never copy old output after editing.
    val panel=TranslationPanel()
    panel.source.text="私は赤い星を観測します。";panel.translateNow()
    check(panel.copy.isEnabled && panel.result.complete)
    panel.swap.doClick();panel.translateNow()
    check(panel.direction.selectedIndex==1 && panel.target.text=="私は赤い星を観測する。")
    panel.source.append(" Unknown el mi.")
    check(!panel.copy.isEnabled && panel.target.text.isEmpty())
    panel.translateNow();check(!panel.result.complete && !panel.copy.isEnabled)
    panel.dispose();passed++
    println("PASS: offline translation $passed checks (30 reviewed examples both directions, new grammar, ambiguity/unknown/rejection, UI stale output)")
}
