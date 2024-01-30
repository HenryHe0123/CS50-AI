import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob = dict()
    if len(corpus[page]) == 0:
        # If page has no links, choose randomly from all pages
        frac = 1 / len(corpus)
        for p in corpus:
            prob[p] = frac
    else:
        frac1 = (1 - damping_factor) / len(corpus)
        frac2 = damping_factor / len(corpus[page])
        for p in corpus:
            prob[p] = frac1
        for p in corpus[page]:
            prob[p] += frac2

    return prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = dict()
    for p in corpus:
        pr[p] = 0
    # Sampling n pages
    random.seed()
    page = random.choice(list(corpus.keys()))
    frac = 1 / n
    for i in range(n):
        pr[page] += frac
        prob = transition_model(corpus, page, damping_factor)
        page = random.choices(list(prob.keys()), list(prob.values()))[0]
    return pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = dict()
    pr_next = dict()
    inverse_n = 1 / len(corpus)
    # Initialize
    for p in corpus:
        pr[p] = inverse_n
        if len(corpus[p]) == 0:
            # If page has no links, view as linking to all pages
            corpus[p] = set(corpus.keys())

    # Iterate until convergence
    # pr(p) = (1 - d) / N + d * sum(pr(i) / NumLinks(i))
    flag = False
    epsilon = 0.00099
    # debug: ~flag would return an integer!
    while not flag:
        flag = True
        for p in corpus:
            pr_next[p] = (1 - damping_factor) * inverse_n
            for i in corpus:
                if p in corpus[i]:
                    pr_next[p] += damping_factor * pr[i] / len(corpus[i])
            # check convergence
            if abs(pr_next[p] - pr[p]) > epsilon:
                flag = False

        # update pr
        for p in corpus:
            pr[p] = pr_next[p]

    return pr


if __name__ == "__main__":
    main()
