from bb_algorithm import BB
from bb_ver2 import BB_ver2
from bb_ver3 import BB_ver3
from test_case import BB_TestCase

#TestCase 2번 -> Maximize 문제
test_case = BB_TestCase(2)

test_case.print_relax()
test_case.print_origin()

bb = BB(test_case.relax_model, test_case.sense)
bb.solve()

bb_ver2 = BB_ver2(test_case.relax_model, test_case.sense)
bb_ver2.solve()

bb_ver3 = BB_ver3(test_case.relax_model, test_case.sense)
bb_ver3.solve()

print('-'*50)

'''
목적: Priority Queue의 정렬 기준에 따라 Iteration 수 변화 확인

결론:
Minimize 에서는 성능 개선이 어느정도 됐다.
Maximize 에서는 성능 개선에 영향이 없었다. 
ver3에서 해가 틀리게 나온다.
'''
print('BB :', end = ' ')
bb.print_result()
print('-'*50)
print('BB_ver2 :', end = ' ')
bb_ver2.print_result()
print('-'*50)
print('BB_ver3 :', end = ' ')
bb_ver3.print_result()
print('-'*50)