def test_checker(answer,target):
    false = []
    true = []
    for i in range(0,len(answer)):
        if answer[i].lower()==target[i].lower():
            true.append(i+1)
        else:
            false.append(i+1)
    
    return {"true":true,
    "false":false}