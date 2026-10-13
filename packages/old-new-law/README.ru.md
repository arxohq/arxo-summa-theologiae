# Ветхий и новый закон (Summa theologiae I-II qq. 98–108)

Пакет `la.aquinas.summa.i_ii_old_new_law` закрепляет Leonina / Corpus Thomisticum
и строит граф quaestio §274 по заголовкам. Прикладной слой применяет *respondeo*:
ветхий закон благ, но несовершенен; естественное содержание обязывает всех,
добавления — только Израиль; церемонии прекращаются во втором статусе; новый
закон — главным образом благодать Святого Духа.

Семейство: [FAMILY.ru.md](../summa-theologiae/FAMILY.ru.md). Решение: DECISION-0325.

## Задачи

| задача | файл | якорь | вход | результат | сценарии |
|---|---|---|---|---|---|
| благ ли ветхий закон | `02-lex-vetus.law` | `ST_I_II_Q98_A1_RESP` | `is_old_law` | `old_law_good` | `tests/01-*.lawtest` |
| сообщает ли благодать | `02-lex-vetus.law` | `ST_I_II_Q98_A1_RESP` | `is_old_law` | `old_law_imperfect` | `tests/02-*.lawtest` |
| обязывает ли естественное содержание | `02-lex-vetus.law` | `ST_I_II_Q98_A5_RESP` | предписание, народ | `binds_as_natural` | `tests/03-*.lawtest` |
| обязывают ли добавления только Израиль | `02-lex-vetus.law` | `ST_I_II_Q98_A5_RESP` | `added_beyond_nature`, `of_israel` | `binds_israel_only` | `tests/04-*.lawtest` |
| культовое ли предписание церемониально | `03-praecepta.law` | `ST_I_II_Q99_A3_RESP` | `for_divine_worship` | `precept_kind(Ceremonial)` | `tests/05-*.lawtest` |
| принадлежат ли моральные естественному закону | `03-praecepta.law` | `ST_I_II_Q100_A1_RESP` | `of_natural_law` | `precept_kind(Moral)` | `tests/11-*.lawtest` |
| прекратились ли церемонии | `03-praecepta.law` | `ST_I_II_Q103_A3_RESP` | культ, `after_christ` | `ceremonial_ceased` | `tests/05-*.lawtest` |
| вложен ли новый закон как благодать | `04-lex-nova.law` | `ST_I_II_Q106_A1_RESP` | благодать Святого Духа | `new_law_indita` | `tests/06-*.lawtest` |
| оправдывает ли новый закон | `04-lex-nova.law` | `ST_I_II_Q106_A2_RESP` | благодать или одна буква | `new_law_justifies` / `new_law_letter_does_not_justify` | `tests/07-*.lawtest`, `tests/08-*.lawtest` |
| один ли конец у нового и ветхого | `04-lex-nova.law` | `ST_I_II_Q107_A1_RESP` | `is_new_law` | `same_end_as_old` | `tests/09-*.lawtest` |
| называется ли евангельский закон законом свободы | `04-lex-nova.law` | `ST_I_II_Q108_A1_RESP` | `is_new_law` | `gospel_is_law_of_liberty` | `tests/10-*.lawtest` |

## Чего пакет не делает, и почему

| граница | почему |
|---|---|
| дата дарования «во время Моисея» | повествование, не вычисляемый срок |
| судебные предписания q. 104–105 как отдельный род в прикладном слое | граф есть; прикладная голова не выделена в этом срезе |
| передоказательство возражений | тела — в закреплённых байтах; граф порождён из заголовков |

Учебные дела: `examples/old-new-cases/`. Каталог вопросов: `QUESTIONS.md`.
