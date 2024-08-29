# Benchmarking Symbolic Execution tools for Wasm

Benchmark Symbolic Execution tools for Wasm

## Datasets

Datasets used can be found here [datasets]

## Experimental Setup


## B-tree Benchmark

Times in the table below are given in seconds.

| Tool | 2o1u.wat | 2o2u.wat | 2o3u.wat | 3o1u.wat | 3o2u.wat | 3o3u.wat | 4o1u.wat | 4o2u.wat | 4o3u.wat | 5o1u.wat | 5o2u.wat | 5o3u.wat | 6o1u.wat | 6o2u.wat | 6o3u.wat | 7o1u.wat | 7o2u.wat | 7o3u.wat | 8o1u.wat | 8o2u.wat | 9o1u.wat | 9o2u.wat |
|-----:|---------:|---------:|---------:|---------:|---------:|---------:|--------:|---------:|---------:|---------:|--------:|---------:|---------:|---------:|--------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
| Manticore | 4.356113433837891 | 35.057982444763184 | 382.6867518424988 | 11.15131163597107 | 110.54555678367615 | 1117.4394385814667 | 17.658937454223633 | 261.1562774181366 | 2713.705121278763 | 33.3046019077301 | 507.3212671279907 | 5722.793907880783 | 67.17487072944641 | 896.0676436424255 | 11118.56573843956 | 97.69167447090149 | 1584.2615401744843 | 20727.641160726547 | 152.3633725643158 | 2567.524380683899 | 210.06907892227173 | 3871.196397781372 |
| Wasp | 0.10400891304 | 0.391007184982 | 3.06230282784 | 0.166229963303 | 0.953495025635 | 10.39884305 | 0.330118894577 | 2.17782998085 | 29.4031460285 | 0.606969833374 | 4.33714818954 | 77.5684869289 | 0.826065063477 | 8.17913293839 | 198.750200033 | 1.45801615715 | 15.5205779076 | 538.423351049 | 2.16484498978 | 29.64843297 | 3.39035391808 | 46.8511180878 |
| Owi | 0.154981136322 | 0.440714120865 | 3.46566820145 | 0.217607021332 | 1.15871596336 | 11.8633778095 | 0.338810920715 | 2.89478302002 | 34.8521339893 | 0.71196603775 | 6.19676399231 | 90.6485219002 | 1.08136200905 | 12.5932309628 | 211.119800806 | 1.95233893394 | 24.683672905 | 460.27963686 | 3.11737704277 | 45.9380779266 | 5.06240296364 | 76.7439870834 |
| Owi_w24 :1st_place_medal: | 0.253731012344 | 0.286954164505 | 0.6017370224 | 0.336513996124 | 0.393337011337 | 1.32598495483 | 0.365776062012 | 0.588371992111 | 3.21399617195 | 0.440592050552 | 0.861088991165 | 7.41016292572 | 0.499325037003 | 1.38547801971 | 16.1416490078 | 0.57300901413 | 2.52830290794 | 32.9235639572 | 0.757837057114 | 4.30031204224 | 0.989750862122 | 6.86542081833 |

## Acknowledgements

We are grateful to Carolina Costa for the B-tree implementation as part
of her M.Sc. [thesis].

[datasets]: datasets/
[thesis]: https://fenix.tecnico.ulisboa.pt/cursos/meic-a/dissertacao/846778572212567
