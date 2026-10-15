package com.reiun.nebulith

data class Entry(val id: Int, val category: String, val nrs: String, val ipa: String,
                 val pos: String, val meaningJa: String, val meaningEn: String, val notes: String)
data class Example(val id: String, val title: String, val nrs: String, val translation: String, val note: String)

object Catalog {
    fun search(entries: List<Entry>, query: String, category: String? = null, pos: String? = null): List<Entry> {
        val words = query.trim().lowercase().split(Regex("\\s+")).filter { it.isNotEmpty() }
        return entries.filter { entry ->
            val matchCategory = category == null || category == entry.category || category == "全カテゴリー"
            val matchPos = pos == null || pos == "すべて" || entry.pos.contains(pos)
            val text = listOf(entry.id.toString(), entry.nrs, entry.ipa, entry.pos,
                entry.meaningJa, entry.meaningEn, entry.notes).joinToString(" ").lowercase()
            matchCategory && matchPos && words.all { it in text }
        }
    }

    fun findRelated(entries: List<Entry>, target: Entry): List<Entry> {
        val stem = target.nrs
        return entries.filter { other ->
            other.id != target.id && (
                other.nrs.startsWith(stem) || 
                other.notes.contains(stem) || 
                (stem.length >= 4 && other.nrs.contains(stem))
            )
        }.take(8)
    }
}
