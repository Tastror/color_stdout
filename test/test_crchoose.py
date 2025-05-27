from crchoose import select_from_list

if __name__ == "__main__":
    sample_items = [str(i) for i in range(2145, 2145 + 103)]
    selected = select_from_list(sample_items)
    print()
    print(f"choosen: {selected}")