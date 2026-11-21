# Native and Cross-Platform UI Reproduction

Use with `image-to-ui` when the target is Flutter, SwiftUI/UIKit, React Native, Jetpack Compose,
Android Views, .NET MAUI, or a desktop shell. The fidelity loop is the same; the units, capture
harness, and platform defaults are not.

Read this together with `frameworks.md` (web frameworks and Tailwind/CSS-in-JS).

## 1. Units and scale

| Platform | Layout unit | Text unit | Physical pixels | Scale source |
| --- | --- | --- | --- | --- |
| Web | CSS px | CSS px | CSS px × DPR | `devicePixelRatio` |
| Flutter | logical px | logical px (with textScaler) | logical × DPR | `MediaQuery.devicePixelRatio` |
| iOS SwiftUI/UIKit | points (pt) | points (with Dynamic Type) | pt × screen scale | `UIScreen.main.scale` / `displayScale` |
| Android Compose/Views | dp | sp (fontScale) | dp × density | `LocalDensity.density` / `displayMetrics.density` |
| React Native | logical px | logical px (font scaling) | logical × PixelRatio | `PixelRatio.get()` |
| .NET MAUI | device-independent units | DIU with font scaling | DIU × density | `DeviceDisplay.MainDisplayInfo.Density` |
| Electron/Tauri | CSS px | CSS px | CSS px × DPR | Chromium `devicePixelRatio` |

Rules:

- **Never compare a 2×/3× screenshot to a 1× render.** Convert to a common unit first.
- **Text scale is a separate variable from density.** iOS Dynamic Type, Android `fontScale`,
  Flutter `textScaler`, and React Native `allowFontScaling` can change wrapping without changing
  the layout unit. Freeze the same setting in the reference and the render.
- **Safe areas and system chrome are not the design** unless the reference includes them.
  Exclude status bars, notches, home indicators, navigation bars, and OS window chrome when
  measuring the content; reproduce them only if the task asks.
- **Points/dp are not CSS px.** A 44pt iOS control and a 44px web control are different physical
  sizes on different devices. Match the reference's unit, not the number alone.

## 2. Platform contract

Add these fields to the skill's step-0 contract:

```
Platform: web / iOS / Android / Flutter / React Native / MAUI / desktop
Unit: CSS px / pt / dp / logical px
Scale: DPR / displayScale / density
Device: [simulator/emulator/browser viewport + OS version]
Text scale: [default / 1.0 / large]
Theme: [light/dark/high contrast]
Safe areas: [included/excluded]
System chrome: [included/excluded]
```

If the reference is a web design but the target is native, decide explicitly:

- **Custom-draw** the surface to match the image (pixel fidelity, less platform convention).
- **Use native controls** (platform behavior and accessibility, not pixel-identical).
- **Hybrid:** native structure, custom styling where the brand requires it.

Document the choice. Do not silently use a native control that looks different and call it
pixel-perfect.

## 3. Capture harnesses

### Flutter

Golden test (recommended for deterministic widget comparison):

```dart
// test/golden_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/dashboard.dart';

void main() {
  testWidgets('dashboard matches reference', (tester) async {
    tester.view.physicalSize = const Size(1440, 900);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(
      const MaterialApp(
        home: MediaQuery(
          data: MediaQueryData(textScaler: TextScaler.noScaling),
          child: Dashboard(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    await expectLater(
      find.byType(Dashboard),
      matchesGoldenFile('goldens/dashboard.png'),
    );
  });
}
```

```bash
flutter test --update-goldens
flutter test
```

- Golden tests render without a device; use `surfaceSize`, `devicePixelRatio`, and a fixed
  `textScaler`.
- Load real fonts in tests (`loadAppFonts` from `golden_toolkit`, or `FontLoader`) or text will
  use Ahem and the diff will be meaningless.
- For a running app/device: `flutter screenshot` (device) or `integration_test` +
  `IntegrationTestWidgetsFlutterBinding.takeScreenshot`.
- `RepaintBoundary.toImage` works for a specific subtree; set `pixelRatio` explicitly.

### SwiftUI

`ImageRenderer` (iOS 16+/macOS 13+) is the most deterministic:

```swift
import SwiftUI
import UIKit

@MainActor
func renderPNG<V: View>(_ view: V, size: CGSize, scale: CGFloat, url: URL) throws {
    let renderer = ImageRenderer(
        content: view
            .frame(width: size.width, height: size.height)
            .environment(\.colorScheme, .light)
            .environment(\.dynamicTypeSize, .large)
    )
    renderer.scale = scale
    guard let image = renderer.uiImage, let data = image.pngData() else {
        throw NSError(domain: "render", code: 1)
    }
    try data.write(to: url)
}
```

- `ImageRenderer` uses points; `scale` maps pt → px (2 or 3 for devices).
- For a running simulator: `xcrun simctl io booted screenshot render.png`; the PNG is in device
  pixels, so divide by the simulator scale for points.
- XCUITest: `XCUIScreen.main.screenshot()` and attach/save the PNG.
- `swift-snapshot-testing` is the standard snapshot harness for SwiftUI/UIKit.
- Set `.environment(\.dynamicTypeSize, ...)`, `.environment(\.colorScheme, ...)`, and locale
  explicitly.

### UIKit

```swift
let format = UIGraphicsImageRendererFormat()
format.scale = UIScreen.main.scale
format.opaque = true
let renderer = UIGraphicsImageRenderer(size: view.bounds.size, format: format)
let image = renderer.image { _ in
    view.drawHierarchy(in: view.bounds, afterScreenUpdates: true)
}
try image.pngData()?.write(to: url)
```

- Lay out first (`layoutIfNeeded`), then draw.
- Use `traitCollection` for scale, display P3, and dark mode.
- `UIFontMetrics` scales fonts with Dynamic Type; test at default and large sizes.
- Snapshot testing via `swift-snapshot-testing` is preferred over hand-rolled drawing.

### Jetpack Compose

Paparazzi (JVM, no emulator) or Roborazzi (Robolectric):

```kotlin
@get:Rule val paparazzi = Paparazzi(
    deviceConfig = DeviceConfig.PIXEL_5.copy(softButtons = false),
    theme = "android:Theme.Material.Light.NoActionBar",
)

@Test fun dashboard() {
    paparazzi.snapshot {
        MaterialTheme {
            Dashboard()
        }
    }
}
```

- Set `fontScale` and `density` explicitly in the device config; both change layout.
- `Modifier.testTag` + `captureToImage()` works on-device but is slower.
- `sp` text scales with the user's font size; use it unless the design explicitly fixes text.

### Android Views / XML

- `dp` for layout, `sp` for text (`android:textSize`), and verify at `fontScale=1.0` and large.
- Use `adb shell wm density` / `wm size` to know the emulator, and
  `adb exec-out screencap -p > render.png` to capture.
- Screenshot tests (e.g., Shot) or Robolectric for JVM snapshots.
- Watch `9-patch`, ripples, elevation shadows, and system bars.

### React Native / Expo

- Layout is flexbox with `flexDirection: "column"` by default; there is no CSS box model.
- `PixelRatio.get()` is the scale; `Dimensions.get("window")` is the logical viewport.
- Text has `allowFontScaling`; freeze it (or test large text) and set `lineHeight` explicitly.
- Capture: Detox `device.takeScreenshot("render")`, Maestro, `react-native-view-shot`, or
  `xcrun simctl io booted screenshot` / `adb exec-out screencap -p`.
- Disable the dev menu/overlay, Fast Refresh banner, and network inspector before capture.
- Use `expo-font`/local fonts; wait for font load and images.

### .NET MAUI

- Device-independent units; `DeviceDisplay.MainDisplayInfo.Density` maps to pixels.
- Capture with Appium/MAUI UITest screenshots or a platform-specific screenshot command.
- Verify `FontAutoScalingEnabled` and platform handlers; native control rendering differs by OS.

### Desktop shells

- **Electron/Tauri:** Chromium rendering; use Playwright or Chrome headless with the exact
  window content size and DPR. Exclude OS title bars unless the reference includes them.
- **macOS AppKit / Windows WinUI:** points/DIPs with display scale; use the platform's snapshot
  APIs and verify at 1× and 2×.

## 4. Framework-specific gotchas

### Flutter

- `TextStyle.height` is a **multiplier** of `fontSize`, not a pixel line-height. Convert from the
  measured line box deliberately.
- `fontSize` is logical px; `textScaler` changes effective size and wrapping.
- Material widgets add default padding/ink/elevation; use `Material`/`Theme` intentionally.
- Shadows use `elevation`, which is not the same as CSS `box-shadow`; custom `BoxShadow` may be
  needed for exact fidelity.
- Golden tests use Ahem unless real fonts are loaded; always load the font.
- Impeller vs Skia can change antialiasing; compare on the target renderer.

### SwiftUI

- `Font.system(size:)` is fixed; `.body`/`.title` scale with Dynamic Type. Match the reference's
  intent, not only the number.
- `@ScaledMetric` for spacing that should scale with text.
- Safe areas and navigation bars add insets; use `.ignoresSafeArea` only if the source does.
- SF Symbols are not the source's custom icons; recreate the path or accept a documented
  substitution.
- `Color` can be P3; convert to sRGB for comparison if the reference is sRGB.
- `.lineSpacing` is extra leading, not total line-height.

### UIKit

- Auto Layout can produce fractional points; compare at device pixels and allow 1px rounding.
- `UILabel` line height and `adjustsFontForContentSizeCategory` affect wrapping.
- `UIScreen.main.scale` is deprecated on newer SDKs; use `traitCollection.displayScale`.
- System colors change with dark mode and accessibility settings; pin the trait collection.

### React Native

- No `box-sizing`; padding/border behavior differs from web.
- `flex: 1` and `minHeight` defaults can collapse or expand differently.
- `Text` inherits differently; nested text is a single native text node.
- `shadow*` props are iOS-only; Android uses `elevation`.
- Font scaling can break a pixel-perfect layout; verify at default and large.

### Jetpack Compose

- `dp` and `sp` are not interchangeable; text in `dp` ignores font scale.
- `MaterialTheme.typography` has its own line heights; override deliberately.
- `Paparazzi` uses a fixed device config; set density/fontScale/orientation.
- Compose preview rendering can differ from device rendering; verify on the target.

### Android Views

- Density buckets and `smallestWidth` change resources; test the target bucket.
- `sp` text grows with font scale; fixed `dp` text is an accessibility trade-off.
- Ripples and elevation are part of the look; decide whether to reproduce them.

## 5. Verification matrix

| Platform | Capture | Status in this repo |
| --- | --- | --- |
| Web HTML/CSS | Chrome headless | **Behaviorally tested** |
| React/Vue/Svelte/Angular | Playwright/Puppeteer | Documented, not tested here |
| Flutter | golden test / integration_test | Documented, not tested here |
| SwiftUI/UIKit | ImageRenderer / simctl / snapshot testing | Documented, not tested here |
| Jetpack Compose | Paparazzi/Roborazzi | Documented; no Android toolchain here |
| React Native | Detox/Maestro/simctl/adb | Documented, not tested here |
| MAUI/desktop | platform capture/Playwright | Documented, not tested here |

A platform is "supported" only when the same reference image has been rendered and diffed on
that platform. Otherwise say "recipe documented; not yet verified."

## 6. Accessibility vs pixel fidelity

Native platforms have user text scaling, dark mode, high contrast, reduced motion, and safe
areas. You cannot freeze them forever to protect a pixel match.

- Reproduce the default state at the reference's settings.
- Verify at large text and dark mode; document where the layout must adapt.
- Do not disable `allowFontScaling`/Dynamic Type just to keep pixels aligned unless the product
  explicitly requires fixed text (and the accessibility cost is accepted).
- Prefer native controls when they provide behavior users depend on; document the visual delta.

## 7. Quality gate additions

- [ ] Platform, unit, scale, device/emulator, text scale, theme, and safe-area policy are stated.
- [ ] The render and reference use the same unit/scale; conversion is shown.
- [ ] Text scaling/Dynamic Type/fontScale is frozen or tested, not ignored.
- [ ] System chrome and safe areas are included/excluded consistently.
- [ ] Native controls vs custom drawing is an explicit decision.
- [ ] The capture harness is deterministic (fonts loaded, animations disabled, dev overlays off).
- [ ] The claim is limited to platforms actually rendered and diffed.
