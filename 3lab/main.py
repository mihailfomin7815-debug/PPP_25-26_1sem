def recursion_permutations(data, story=None, cur_iter=0, path=None):
    if story is None:
        story = []
    if path is None:
        path = []
    story.append({'data': data, 'path': path.copy(), 'cur_iter':cur_iter})
    if isinstance(data, dict):
        for key, val in data.items():
            recursion_permutations(val, story, cur_iter + 1, path + [key])
    if isinstance(data, list):
        for ind,val in enumerate(data):
            recursion_permutations(val, story, cur_iter + 1, path + [ind])
    return story

def print_story(json):
    story = recursion_permutations(json)
    for stage in story:
        print(stage)

json =  {'a': [1, 2],'b': {'x': 10, 'y': 20}}

if __name__ == "__main__":
    print_story(json)
