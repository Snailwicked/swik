import os
class ScalableBloomFilter:
    pass

def url_bloomfilter(verify_text):
    is_exist = os.path.exists('news.blm')
    if is_exist:
        bf = ScalableBloomFilter.fromfile(open('news.blm', 'rb'))
        if verify_text in bf:
            return ""
        else:
           return verify_text
    return verify_text

def url_add(url):
    is_exist = os.path.exists('news.blm')
    if is_exist:
        bf = ScalableBloomFilter.fromfile(open('news.blm', 'rb'))
        bf.add(url)
        bf.tofile(open('news.blm', 'wb'))
    else:
        bf = ScalableBloomFilter(initial_capacity=1000000, error_rate=0.00001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        bf.add(url)
        bf.tofile(open('news.blm', 'wb'))


def filterURL(url):
    newurl = url_bloomfilter(url)
    url_add(url)
    return newurl


if __name__ == "__main__":
    verify_text = ["b","c","d","e"]
    for i in verify_text:
        print(filterURL(i))
