[![Security Pipeline](https://github.com/GuillaumeFalourd/formulas-games/actions/workflows/security_pipeline.yml/badge.svg)](https://github.com/GuillaumeFalourd/formulas-games/actions/workflows/security_pipeline.yml)

# Formulas Games

![title](https://user-images.githubusercontent.com/22433243/119173001-fd92ea00-ba3c-11eb-9314-bad231c0bbc3.png)


## 📚 Documentation

This repository contains Ritchie formulas which can be executed by [ritchie-cli](https://github.com/ZupIT/ritchie-cli).

- [Ritchie CLI documentation](https://docs.ritchiecli.io)


## 🔎 What you'll find in this repository

- [Flappy Bird Game](https://github.com/GuillaumeFalourd/formulas-python/tree/master/game/flappy-bird): `rit game flappy-bird`

![Game](/docs/img/rit-game-flappy-bird-play.png)

- [Pacman Game](https://github.com/GuillaumeFalourd/formulas-python/tree/master/game/pacman): `rit game pacman`

![Game](/docs/img/rit-game-pacman-play.png)

- [Snake Game](https://github.com/GuillaumeFalourd/formulas-python/tree/master/game/snake): `rit game snake`

![Game](/docs/img/rit-game-snake-play.png)

- [Space Invasion Game](https://github.com/GuillaumeFalourd/formulas-python/tree/master/game/space-invasion): `rit game space-invasion`

![Game](/docs/img/rit-game-space-invasion-play.png)

## 📦 Use Formulas

To import this repository, you need [Ritchie CLI installed](https://docs.ritchiecli.io/getting-started/install-cli)

Then, you can use the `rit add repo` command manually, or execute the command line below directly on your terminal (since CLI version 2.8.0):

```bash
rit add repo --provider="Github" --name="formulas-games" --repoUrl="https://github.com/GuillaumeFalourd/formulas-games" --priority=1
```

Finally, you can check if the repository has been imported correctly by executing the `rit list repo` command.

## ♻️ Contribute to the repository

### 🆕 Creating formulas

1. Fork and clone the repository
2. Create a branch: `git checkout -b <branch_name>`
3. Check the step by step of [how to create formulas on Ritchie](https://docs.ritchiecli.io/tutorials/formulas/how-to-create-formulas)
4. Add your formulas to the repository
and commit your implementation: `git commit -m '<commit_message>`
5. Push your branch: `git push origin <project_name>/<location>`
6. Open a pull request on the repository for analysis.

### 🆒 Updating Formulas

1. Fork and clone the repository
2. Create a branch: `git checkout -b <branch_name>`
3. Add the cloned repository to your workspaces (`rit add workspace`) with a highest priority (for example: 1).
4. Check the step by step of [how to implement formulas on Ritchie](https://docs.ritchiecli.io/tutorials/formulas/how-to-implement-a-formula)
and commit your implementation: `git commit -m '<commit_message>`
5. Push your branch: `git push origin <project_name>/<location>`
6. Open a pull request on the repository for analysis.

- [Contribute to Ritchie community](https://github.com/ZupIT/ritchie-formulas/blob/master/CONTRIBUTING.md)
