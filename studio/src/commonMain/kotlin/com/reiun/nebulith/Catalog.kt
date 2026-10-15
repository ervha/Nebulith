package com.reiun.nebulith

data class Entry(val id: Int, val category: String, val nrs: String, val ipa: String,
                 val pos: String, val meaningJa: String, val meaningEn: String, val notes: String)
data class Example(val id: String, val title: String, val nrs: String, val translation: String, val note: String)

object Catalog {
    fun search(entries: List<Entry>, query: String, category: String? = null): List<Entry> {
        val words = query.trim().lowercase().split(Regex("\\s+")).filter { it.isNotEmpty() }
        return entries.filter { entry ->
            val text = listOf(entry.id.toString(), entry.nrs, entry.ipa, entry.pos,
                entry.meaningJa, entry.meaningEn, entry.notes).joinToString(" ").lowercase()
            (category == null || category == entry.category) && words.all { it in text }
        }
    }
}
