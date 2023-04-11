# Manual Test Sensei 🐱‍👤
Manual Test Sensei is a tool for detecting "test smells" in manual testing. Test smells are patterns of poor testing practices that can lead to ineffective or incomplete testing. By identifying and addressing these issues, Manual Test Sensei can help improve the quality and effectiveness of manual testing.

The smells identified by our Sensei are based on the paper [Hunting for smells in natural language tests](https://ieeexplore.ieee.org/document/6606682/), by _Hauptmann et al._, on the [Open Test Smells Catalog](https://easy.github.io/testsmells/index.html), and on the tool creators' expertise on the subject.

This repository is divided in two main folders. `\ManualTestSensei\` which is our tool, `\testcases\` where the UbuntuOS testcases are located.

## `\ManualTestSensei\`

This folder contains the tool and it's packages. There's a `README.md` inside it, guiding the reader on how to use the tool. If you want to run the tool, enter this folder.

## `\testcases\`
This folder contains the manual testcases utilized by the quality team for testing ubuntu (and its flavors) packages and images, as well as manual tests for hardware compatibility. It's a fork of [Ubuntu Manual Tests](https://launchpad.net/ubuntu-manual-tests) that has been analyzed in search of test smells. If you want to see how a manual test is written, enter this folder.

