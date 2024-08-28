# Benchmarking Symbolic Execution tools for Wasm

Benchmark Symbolic Execution tools for Wasm

## Datasets

Datasets used can be found here [datasets]

## Experimental Setup


## B-tree Benchmark

| Tool | 8o2u.wat | 6o2u.wat | 5o1u.wat | 2o1u.wat | 4o3u.wat | 8o1u.wat |3o2u.wat | 2o3u.wat | 3o3u.wat | 3o1u.wat |9o2u.wat | 2o2u.wat | 5o3u.wat | 4o2u.wat |9o1u.wat | 7o1u.wat | 4o1u.wat | 7o2u.wat | 7o3u.wat | 5o2u.wat | 6o3u.wat | 6o1u.wat |
|-----:|---------:|---------:|---------:|---------:|---------:|---------:|--------:|---------:|---------:|---------:|--------:|---------:|---------:|---------:|--------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
| wasp | 29.1863 | 8.24894 | 0.607853 | 0.0781879 | 29.2891 | 2.23006 | 0.953961 | 3.01175 | 10.2708 | 0.166423 | 46.5307 | 0.425192 | 77.5291 | 2.23068 | 3.6062 | 1.41814 | 0.32165 | 15.5922 | 543.205 | 4.37109 | 199.425 | 0.889558 |
| owi | 45.752 | 12.4428 | 0.713889 | 0.169405 | 35.0763 | 3.15453 | 1.17274 | 3.43007 | 12.011 | 0.235351 | 78.6858 | 0.451845 | 90.4215 | 2.92894 | 5.1349 | 1.95023 | 0.397887 | 24.7686 | 463.364 | 6.2392 | 211.234 | 1.09871|
| owi_w20 | 4.35252 | 1.37144 | 0.424698 | 0.27149 | 3.21998 | 0.67546 | 0.376411 | 0.59001 | 1.28906 | 0.297261 | 6.90641 | 0.32656 | 7.40522 | 0.59537 | 1.01032 | 0.596163 | 0.39274 | 2.51705 | 32.9564 | 0.762938 | 16.2011 | 0.491792 |

## Acknowledgements

We are grateful to Carolina Costa for the B-tree implementation as part
of her M.Sc. [thesis].

[datasets]: datasets/
[thesis]: https://fenix.tecnico.ulisboa.pt/cursos/meic-a/dissertacao/846778572212567
