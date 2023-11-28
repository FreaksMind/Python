def merge(files, order, separator, output_file):
    count_chars = 0

    if order is not None and len(order) != 0: 
        files = sorted(files, key=lambda x: order.index(x) if x in order else float('inf'))

    with open(output_file, 'w') as o:
        for file in files:
            with open(file, 'r') as f:
                file_content = f.read()
                o.write(file_content)
                o.write(separator)
                count_chars += len(file_content)


    return f"Written {len(files)} files to {output_file} with a total of {count_chars} characters."