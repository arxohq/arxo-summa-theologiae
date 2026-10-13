# Вопросы к пакету `la.aquinas.duplex_effectus`

<!-- Порождено из analysis/questions.json: python3 verify/ci/gates/coverage/check_package_questions.py --emit. Не править руками. -->

Каталог **предусмотренных** запросов §172 и того, чем каждый проверен (DECISION-0190). Карточка не означает положительного ответа по делу: ответ даёт только evaluation-документ с доказательством. Отсутствие карточки означает «не описано каталогом», а не «право молчит».

## Самооборона и двойной эффект (II-II q. 64 a. 7)

Единицы источника: ST_Q64_A7_RESP.

| id | вопрос | форма | цель | шаблон | ветви | проверено |
|---|---|---|---|---|---|---|
| `defensio-licita` | Установлено ли, что «оборона дозволена» (a: предъявленное действие обороны a)?<br>*авторская формулировка:* Дозволена ли предъявленная оборона? | truth | `defensio_licita(a: Actus)` | `evaluate truth(defensio_licita(a: <a>));` | частная оборона: намерение сохранить жизнь, сила соразмерна, смерть не цель и не средство (`DefensioLicitaPrivata`); публичная власть относит намеренное поражение к общему благу (`DefensioPubliciMinistri`) | тестов 4; дел ViatorContraLatronem, MilesContraHostes; вопросов `viator-defensio-licita.json`, `miles-defensio-licita.json` |
| `defensio-illicita` | Установлено ли, что «оборона недозволена» (a: предъявленное действие обороны a)?<br>*авторская формулировка:* Недозволена ли предъявленная оборона? | truth | `defensio_illicita(a: Actus)` | `evaluate truth(defensio_illicita(a: <a>));` | сила больше, чем требует мера безупречной защиты (`ImmoderataViolentiaIllicita`); намеренное убийство делает оборону недозволенной (`OccisioRedditDefensionemIllicitam`); служитель публичной власти движим частной страстью (`PrivataLibidoMinistriPeccat`) | тестов 2; дел FamiliaNocte; вопросов `familia-defensio-illicita.json` |
| `pochemu-ne-licita` | Почему не установлено, что «оборона дозволена» (a: предъявленное действие обороны a)?<br>*авторская формулировка:* Почему предъявленная оборона не дозволена: какой посылки не хватает? | why_not | `defensio_licita(a: Actus)` | `evaluate why_not(defensio_licita(a: <a>));` | — | дел FamiliaNocte; вопросов `familia-pochemu-ne-licita.json` |
| `occisio-illicita` | Установлено ли, что «намеренное убийство в обороне недозволено» (a: предъявленное действие обороны a)?<br>*авторская формулировка:* Недозволено ли намеренное убийство в этой обороне? | truth | `occisio_illicita(a: Actus)` | `evaluate truth(occisio_illicita(a: <a>));` | частное лицо намерено убить (`OccisioIntentaPrivatoIllicita`); смерть как средство, не praeter intentionem (`OccisioUtMediumIllicita`) | тестов 1 |
| `pozitsii-defensio` | Какие нормативные позиции возникли по делу (нормы: «дозволенная оборона открывает свободу защищать себя») и каков их статус?<br>*авторская формулировка:* Открыта ли позиция дозволенной самообороны? | positions | нормы `DefensioPropria` | `evaluate positions(); expect position(DefensioPropria, <статус>);` | — | тестов 2; дел ViatorContraLatronem; вопросов `viator-positions.json` |
| `pozitsii-occisio` | Какие нормативные позиции возникли по делу (нормы: «частному лицу в ситуации обороны запрещено иметь целью убийство») и каков их статус?<br>*авторская формулировка:* Запрещено ли частному лицу иметь целью убийство в этой обороне? | positions | нормы `OccisioIntentaInDefensione` | `evaluate positions(); expect position(OccisioIntentaInDefensione, <статус>);` | — | тестов 4; дел ViatorContraLatronem, FamiliaNocte; вопросов `viator-positions.json`, `familia-positions.json` |
| `pozitsii-defensio-vetita` | Какие нормативные позиции возникли по делу (нормы: «недозволенная оборона запрещает защищаться этим действием») и каков их статус?<br>*авторская формулировка:* Запрещена ли предъявленная недозволенная оборона? | positions | нормы `DefensioIllicitaProhibita` | `evaluate positions(); expect position(DefensioIllicitaProhibita, <статус>);` | — | тестов 2; дел FamiliaNocte; вопросов `familia-positions.json` |

- **Не отвечает:** Исполняется ли граф возражений артикула? — источник отсылает вовне (ST_Q64_A7_ARG1). Граф возражений, sed contra и ответов ad не исполняется: он уже построен в пакете la.aquinas.summa_theologiae_law; здесь применяется только формулировка respondeo.
- **Не отвечает:** Вычисляется ли численный порог соразмерной силы? — нужны данные, которые приносит дело (ST_Q64_A7_RESP). Соразмерность силы (moderamen inculpatae tutelae) не вычисляется: артикул численного порога не содержит и отдаёт признак практическому суждению §47.3. Связанный вопрос: `defensio-licita`.
- **Не отвечает:** Наступает ли irregularitas клирика? — источник отсылает вовне (ST_Q64_A7_AD3). Irregularitas клирика после человекоубийства, даже безгрешного, не моделируется: каноническое последствие вне среза моральной квалификации акта.

## Справедливая война (II-II q. 40 a. 1)

Единицы источника: ST_Q40_A1_RESP.

| id | вопрос | форма | цель | шаблон | ветви | проверено |
|---|---|---|---|---|---|---|
| `bellum-iustum` | Установлено ли, что «война справедлива» (b: предъявленная война как предмет оценки b)?<br>*авторская формулировка:* Справедлива ли предъявленная война? | truth | `bellum_iustum(b: Bellum)` | `evaluate truth(bellum_iustum(b: <b>));` | три условия: власть государя, справедливая причина, правое намерение (`BellumIustumConstat`) | тестов 1; дел PrincepsCupiditas; вопросов `princeps-bellum-iustum.json` |
| `bellum-illicitum` | Установлено ли, что «война недозволена» (b: предъявленная война как предмет оценки b)?<br>*авторская формулировка:* Недозволена ли война из-за порочного намерения? | truth | `bellum_illicitum(b: Bellum)` | `evaluate truth(bellum_illicitum(b: <b>));` | власть и справедливая причина есть, намерение порочно (`PravaIntentioRedditBellumIllicitum`) | тестов 1; дел PrincepsCupiditas; вопросов `princeps-bellum-illicitum.json` |
| `pozitsii-bellum` | Какие нормативные позиции возникли по делу (нормы: «при трёх условиях государь вправе вести войну») и каков их статус?<br>*авторская формулировка:* Вправе ли государь вести эту войну? | positions | нормы `BellumIustumGerere` | `evaluate positions(); expect position(BellumIustumGerere, <статус>);` | — | тестов 1 |
| `pozitsii-bellum-vetitum` | Какие нормативные позиции возникли по делу (нормы: «война, ставшая недозволенной, запрещает государю её вести») и каков их статус?<br>*авторская формулировка:* Запрещено ли государю вести эту недозволенную войну? | positions | нормы `BellumIllicitumGerere` | `evaluate positions(); expect position(BellumIllicitumGerere, <статус>);` | — | тестов 3; дел PrincepsCupiditas; вопросов `princeps-bellum-positions.json` |

- **Не отвечает:** Передоказывается ли теорема справедливой войны? — ограничение языка или движка (ST_Q40_A1_RESP). Тела доказательств возражений остаются в закреплённых байтах; пакет не передоказывает теорему, а применяет принятую формулировку к делу.

## Итог

Карточек 11, границ 4, внутренних звеньев 0; выводимых предикатов в CLIR 5, норм 5 — поверхность закрыта в обе стороны. Причины по конкретному делу берутся не из каталога, а из issues и why_not ответа.
