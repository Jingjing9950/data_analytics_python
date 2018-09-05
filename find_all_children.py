parent = ["",'1','2','11','111','11','4','44']
child = ['1','11','12','111','1111','12','44','444']
dic = {}
for i in range(len(parent)):
    if parent[i] not in dic:
        dic[parent[i]] = [child[i]]
    else:
        dic[parent[i]] += [child[i]]

print(dic)

input_value = '444'
result = []
tem_result = [input_value]
while tem_result:
    for x in tem_result:
        tem_result.remove(x)
        if x in dic:
            result += dic[x]
            tem_result += dic[x]


print(result)
