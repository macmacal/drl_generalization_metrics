# Metrics for Assessing Generalization of Deep Reinforcement Learning in Parameterized Environments
### [Paper](https://sciendo.com/article/10.2478/jaiscr-2024-0003)

> "Metrics for Assessing Generalization of Deep Reinforcement Learning in Parameterized Environments"<br/>
> [Maciej Aleksandrowicz](https://macmacal.github.io), [Joanna Jaworek-Korjakowska](https://home.agh.edu.pl/~jaworek/)<br/>
> [Machine Vision Group](https://home.agh.edu.pl/~mdig/) 2023


This repository contains code for the research article.

## Running the project container
The all dependencies of this project are packed into a single [Docker Container](https://www.docker.com/resources/what-container/).

TL;DR for your convenience: to run this project, you only need to install [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/) on your machine. The project have been developed and tested on `Ubuntu 22.04` and `Arch Linux`.

After obtaining working `Docker Engine` & `Docker Compose`:

1. Create the project workspace directory (i.e. `/home/$USER/drl_ws` or just clone this repoistory). Move all code files to that directory. 
2. In the project folder, enter the `docker` subdirectory.
3. Edit the bind-mount paths in `docker-compose.yaml` file (i.e. change `/home/macal/paper_ws` to your's project path). You need to specify the workspace directory, `zshrc` and `zsh_history` files.
4. Inside the `docker` subdirectory, build and run the container:
```bash
docker-compose build
docker-compose up
```
5. The entrypoint of the project will start a local Jupyter Lab instance. Please click on the link inside the terminal to proeced further.



---

## Citation
If you find this code useful for your research, please cite our work with the following [BibTeX entry](./CITATION.bib):

```bibtex
@article{Aleksandrowicz2023,
    author = {Maciej Aleksandrowicz and Joanna Jaworek-Korjakowska},
    doi = {doi:10.2478/jaiscr-2024-0003},
    url = {https://doi.org/10.2478/jaiscr-2024-0003},
    title = {Metrics for Assessing Generalization of Deep Reinforcement Learning in Parameterized Environments},
    journal = {Journal of Artificial Intelligence and Soft Computing Research},
    number = {1},
    volume = {14},
    year = {2023},
    pages = {45--61}
}
```

For your convenience, here is the citation in MLA formatting:
> Aleksandrowicz, Maciej and Jaworek-Korjakowska, Joanna. "Metrics for Assessing Generalization of Deep Reinforcement Learning in Parameterized Environments" Journal of Artificial Intelligence and Soft Computing Research, vol.14, no.1, 2023, pp.45-61. https://doi.org/10.2478/jaiscr-2024-0003

---

Contact: [MVG Group Website](https://home.agh.edu.pl/~mdig/)

