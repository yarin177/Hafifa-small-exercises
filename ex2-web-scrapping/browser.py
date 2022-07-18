import os

def main():
    if not os.path.isdir("output"):
        os.mkdir("output")

    urls = open('input//urls.input','r').read().split('\n')
    for i in range(len(urls)):
        os.mkdir('output//' + str(i+1) +  '_url')


if __name__ == "__main__":
    main()