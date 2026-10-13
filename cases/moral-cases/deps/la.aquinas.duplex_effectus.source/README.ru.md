# Самооборона и справедливая война (Summa theologiae II-II)

Пакет `la.aquinas.duplex_effectus` применяет respondeo Фомы Аквинского:

- II-II q. 64 a. 7 — принцип двойного эффекта и мера безупречной защиты;
- II-II q. 40 a. 1 — три условия справедливой войны.

Доказательства возражений остаются в закреплённых байтах. Пакет отвечает на
предъявленное действие, а не передоказывает артикул.

## Задачи

| задача | файл | якорь | вход | результат | сценарии |
|---|---|---|---|---|---|
| дозволена ли частная оборона | `02-duplex-effectus.law` | `ST_Q64_A7_RESP` | действие, намерение, суждение о мере | `defensio_licita`, позиция `DefensioPropria` | `tests/01-*.lawtest`, `tests/08-*.lawtest` |
| превышена ли мера силы | `02-duplex-effectus.law` | `ST_Q64_A7_RESP` | `vis_moderata` (суждение §47.3) | `defensio_illicita` или `REQUIRES_JUDGMENT`; запрет `DefensioIllicitaProhibita` | `tests/02-*.lawtest`, `tests/05-*.lawtest`, `tests/12-*.lawtest` |
| намеренное убийство частным лицом | `02-duplex-effectus.law` | `ST_Q64_A7_RESP` | `intentio_occisionis` | `occisio_illicita`; запрет `OccisioIntentaInDefensione` | `tests/03-*.lawtest`, `tests/11-*.lawtest` |
| воин / служитель судьи | `02-duplex-effectus.law` | `ST_Q64_A7_RESP` | публичная власть и отнесение к общему благу | `defensio_licita`; запрета `OccisioIntentaInDefensione` нет | `tests/04-*.lawtest`, `tests/11-*.lawtest` |
| справедлива ли война | `03-bellum-iustum.law` | `ST_Q40_A1_RESP` | три условия | `bellum_iustum`, позиция `BellumIustumGerere` | `tests/06-*.lawtest`, `tests/09-*.lawtest` |
| недозволенная война | `03-bellum-iustum.law` | `ST_Q40_A1_RESP` | порочное намерение при власти и причине | `bellum_illicitum`; запрет `BellumIllicitumGerere` | `tests/07-*.lawtest`, `tests/13-*.lawtest` |

## Чего пакет не делает, и почему

| граница | почему |
|---|---|
| граф возражений §274 | уже построен в `la.aquinas.summa_theologiae_law` |
| численный порог соразмерности | артикул его не называет; канал — суждение §47.3 |
| irregularitas клирика | каноническое последствие вне моральной квалификации акта |
| передоказательство теоремы | тела доказательств — в закреплённых байтах |

Учебные дела: `examples/moral-cases/`. Каталог вопросов: `QUESTIONS.md`.
