# compression_algorithms

## arithmetic_coding

В коде есть константа STEP_SIZE отвечающая за размер блоков кодирования, и чем она больше, тем лучше результат, в размен на время работы.

Тестировался алгоритм на ASCII текстах, которые можно найти в файлах data.txt и big_data.txt.

Использование:

В коде есть константа BLOCK_SIZE отвечающая за размер блоков кодирования, и чем она больше, тем лучше результат, в размен на время работы.

Тестировался алгоритм на ASCII текст t, которыq можно найти в файле data.txt.

```
python3 main.py c input_file out_file
python3 main.py d out_file out_file
```

## bwt_rle_coding
