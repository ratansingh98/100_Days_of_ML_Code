output_file_location = 'model/output_dev_921'
tst_file_location = 'data/tst2013.bpe.from'

if __name__ == '__main__':
    with open(output_file_location, "r") as f:
        content = f.read()
        to_data = content.split('\n')

    with open(tst_file_location, "r") as f:
        content = f.read()
        content = content.replace('▁',' ').replace('  ',' ')
        print(content)
        from_data = content.split('\n')

    for n, _ in enumerate(to_data[:-1]):
        print(30*'_')
        print('>', from_data[n])
        print()
        print('Reply:', to_data[n])
