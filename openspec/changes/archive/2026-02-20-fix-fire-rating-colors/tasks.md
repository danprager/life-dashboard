## 1. Write Colour Tests (red)

- [x] 1.1 Add a test asserting Moderate badge background is `#6DB840`
- [x] 1.2 Add a test asserting High badge background is `#F7D94A`
- [x] 1.3 Add a test asserting Extreme badge background is `#E87820`
- [x] 1.4 Add a test asserting Catastrophic badge background is `#922B21`
- [x] 1.5 Add a test asserting No Rating badge background is `#FFFFFF` with black text
- [x] 1.6 Add a test asserting an unknown rating falls back to `#888888`

## 2. Write Popup Tests (red)

- [x] 2.1 Add a test asserting the `?` button is present when `fire_danger` is non-null
- [x] 2.2 Add a test asserting the help dialog opens when the `?` button is clicked
- [x] 2.3 Add a test asserting the dialog contains all five AFDRS rating labels

## 3. Confirm Red

- [x] 3.1 Run `npm run test:unit` — confirm all new tests fail

## 4. Build Popup (with current colours)

- [x] 4.1 Add a `?` icon button next to the Fire Danger Ratings label, visible only when the FDR row is shown
- [x] 4.2 Add a Vuetify dialog triggered by the `?` button
- [x] 4.3 Populate the dialog with stacked bands for all five AFDRS ratings, driven by `FDR_COLOURS`
- [x] 4.4 Run `npm run test:unit` — popup tests (2.1–2.3) pass; colour tests (1.1–1.6) still fail

## 5. Fix Colour Map (green)

- [x] 5.1 Replace `FDR_COLOURS` with the five AFDRS ratings and sampled hex values
- [x] 5.2 Update the badge inline style to use black text for High and No Rating, white for all others
- [x] 5.3 Run `npm run test:unit` — all tests pass; popup automatically reflects correct colours
