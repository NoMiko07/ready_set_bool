from powerset_class import powerset

def main():
    B = powerset([1, 2, 3])
    for sets in B:
        print (sets)

if __name__ == "__main__":
    main()