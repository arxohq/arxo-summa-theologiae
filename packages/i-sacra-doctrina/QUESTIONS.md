# Вопросы к пакету `la.aquinas.summa.i_sacra_doctrina`

<!-- Порождено из analysis/questions.json: python3 verify/ci/gates/coverage/check_package_questions.py --emit. Не править руками. -->

Каталог **предусмотренных** запросов §172 и того, чем каждый проверен (DECISION-0190). Карточка не означает положительного ответа по делу: ответ даёт только evaluation-документ с доказательством. Отсутствие карточки означает «не описано каталогом», а не «право молчит».

## I qq. 1-1: священное учение

Единицы источника: ST_I_Q1_A1_RESP, ST_I_Q1_A2_RESP, ST_I_Q1_A8_RESP.

| id | вопрос | форма | цель | шаблон | ветви | проверено |
|---|---|---|---|---|---|---|
| `sacreddoctrinenecessary` | Установлено ли, что «помимо философии необходимо иное учение» (s: предъявленный предмет respondeo s)?<br>*авторская формулировка:* Необходимо ли священное учение? | truth | `doctrine_necessary(s: Subject)` | `evaluate truth(doctrine_necessary(s: <s>));` | условия respondeo налицо (`SacredDoctrineNecessary`); нет отличительного факта (`SacredDoctrineNecessary`) | тестов 2 |
| `sacreddoctrineisscience` | Установлено ли, что «священное учение есть наука» (s: предъявленный предмет respondeo s)?<br>*авторская формулировка:* Есть ли священное учение наукой? | truth | `doctrine_is_science(s: Subject)` | `evaluate truth(doctrine_is_science(s: <s>));` | условия respondeo налицо (`SacredDoctrineIsScience`); нет отличительного факта (`SacredDoctrineIsScience`) | тестов 2 |
| `sacreddoctrineargumentative` | Установлено ли, что «это учение пользуется доводами» (s: предъявленный предмет respondeo s)?<br>*авторская формулировка:* Пользуется ли священное учение доводами? | truth | `doctrine_argues(s: Subject)` | `evaluate truth(doctrine_argues(s: <s>));` | условия respondeo налицо (`SacredDoctrineArgumentative`); нет отличительного факта (`SacredDoctrineArgumentative`) | тестов 2 |

- **Не отвечает:** Исполняется ли граф возражений как прикладной канон? — источник отсылает вовне (ST_I_Q1_A1_RESP). Граф возражений §274 порождается из заголовков Corpus (arg./s. c./co./ad N) и не является прикладным каноном respondeo.
- **Не отвечает:** Передоказывается ли теорема артикула? — источник отсылает вовне (ST_I_Q1_A1_RESP). Тела доказательств возражений остаются в закреплённых байтах; пакет не передоказывает теорему, а применяет принятую формулировку к делу.
- **Не отвечает:** Выделена ли прикладная голова у каждого артикула? — норма есть в тексте, правил ещё нет (ST_I_Q1_A1_RESP). Артикулы без отдельной прикладной головы имеют граф §274; прикладной слой читает избранные respondeo трактата, не каждый артикул.

## Выводимое без собственной карточки

Звенья вывода: спрашиваются через карточки выше, названы здесь ради полноты поверхности в обе стороны.

| предикат | почему без карточки |
|---|---|
| `q1_a10_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_ad3_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_arg3_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_reply3` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a10_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_arg1_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_arg2_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a1_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_arg1_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_arg2_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a2_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a3_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a3_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a3_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a3_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a3_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a3_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a3_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a3_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a4_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a4_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a4_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a4_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a4_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a4_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a4_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a4_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_arg1_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_arg2_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a5_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_ad3_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_arg1_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_arg2_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_arg3_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_reply3` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a6_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_arg1_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_arg2_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a7_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a8_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a8_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a8_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a8_arg1_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a8_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a8_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a8_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a8_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a8_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_ad1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_ad2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_ad3_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_arg1_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_arg2_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_arg2_premise2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_arg3_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_reply1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_reply2` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_reply3` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_respondeo_premise1` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |
| `q1_a9_thesis` | граф §274 артикула: спрашивается профилем argumentation, не прикладной карточкой respondeo |

## Итог

Карточек 3, границ 3, внутренних звеньев 101; выводимых предикатов в CLIR 104, норм 0 — поверхность закрыта в обе стороны. Причины по конкретному делу берутся не из каталога, а из issues и why_not ответа.
