# iOS 6 Apps

Small open-source apps for iPhones that are stuck on **iOS 6** (written for an iPhone 5 on iOS 6.1.3, armv7), built with a current Mac toolchain.
They are drawn in code in the skeuomorphic style of the era and need no server of their own. Where iOS 6's old TLS stack cannot talk to today's web,
the app carries its own ([Mbed TLS](https://github.com/Mbed-TLS/mbedtls)).

| | App | What it does | Download |
|---|---|---|---|
| <img src="https://raw.githubusercontent.com/ios6-apps/ios6-hnreader/main/res/Icon@2x.png" width="57" alt=""> | **[HN Reader](https://github.com/ios6-apps/ios6-hnreader)** | Hacker News reader with article reader view, threaded comments and offline saved stories. Own TLS 1.2 stack. | [Releases](https://github.com/ios6-apps/ios6-hnreader/releases) |
| <img src="https://raw.githubusercontent.com/ios6-apps/ios6-redditreader/main/res/Icon@2x.png" width="57" alt=""> | **[Reddit Reader](https://github.com/ios6-apps/ios6-redditreader)** | Reddit from the logged-out Atom feeds: pictures, GIFs and v.redd.it video (joined on the phone), saved posts. Respects Reddit's rate limit. | [Releases](https://github.com/ios6-apps/ios6-redditreader/releases) |
| <img src="https://raw.githubusercontent.com/ios6-apps/ios6-kodiremote/main/res/Icon@2x.png" width="57" alt=""> | **[Kodi Remote](https://github.com/ios6-apps/ios6-kodiremote)** | Remote control for Kodi over JSON-RPC: d-pad, play/pause, seek, volume, add-on shortcuts and typing into Kodi's text boxes. | [Releases](https://github.com/ios6-apps/ios6-kodiremote/releases) |
| <img src="https://raw.githubusercontent.com/ios6-apps/ios6-tumbler/main/res/Icon@2x.png" width="57" alt=""> | **[Tumbler](https://github.com/ios6-apps/ios6-tumbler)** | TOTP/HOTP authenticator with QR scanning, Google Authenticator import and a PIN lock. Read its security notes first. | [Releases](https://github.com/ios6-apps/ios6-tumbler/releases) |
| <img src="https://raw.githubusercontent.com/ios6-apps/ios6-tvremote/main/res/Icon@2x.png" width="57" alt=""> | **[TV Remote](https://github.com/ios6-apps/ios6-tvremote)** | Wood-and-plastic remote for Android TV / Google TV (Remote protocol v2), with pairing done on the phone. *Not yet verified against a real TV.* | [Releases](https://github.com/ios6-apps/ios6-tvremote/releases) |

## Installing

Every push to `main` is built by GitHub Actions. Download the unsigned `.ipa` from a repository's **Releases** page: the versioned release is the stable one,
`nightly` is the newest build of `main`. The IPAs are **unsigned**, so the phone needs a jailbreak and
[AppSync Unified](https://github.com/akemin-dayo/AppSync). Then, for example:

    ideviceinstaller -i Tumbler-1.0.0.ipa

(`ideviceinstaller` comes from [libimobiledevice](https://libimobiledevice.org/), `brew install ideviceinstaller`.)

## Building and contributing

Each repository builds on a Mac with Xcode: `tools/setup-sdk.sh` fetches the iOS 9.3 SDK stubs that current Xcode needs for an armv7 / iOS 6 target, then `./build.sh device`
makes the IPA and `./build.sh sim` makes a simulator build. The repositories also carry a `CLAUDE.md`, so a coding agent can build, test and fix them too.
Issues and pull requests are welcome; please say which device and iOS version you tried. Everything is MIT-licensed, with third-party notices in each repository.

These are independent projects, not affiliated with Hacker News / Y Combinator, Reddit, the Kodi Foundation, Google or any other service they talk to.

## Branding

`branding/` holds the organization logo (`logo.png`), a 1280x640 social preview image for each repository (`social/`) and the script that draws them (`make_branding.py`, needs Pillow and macOS fonts).
The app icons live in each app's `docs/icon.png`.
