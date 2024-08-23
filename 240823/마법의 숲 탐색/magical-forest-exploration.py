def p(A,er,ec):
    for r,l in enumerate(A):
        for c,e in enumerate(l):
            if (r,c)==(er, ec):
                print("@", end=' ')
                continue
            if e==0:
                print(".", end=' ')
            else:
                print(e, end=' ')
        print()
    print()

def solution():
    R, C, K = map(int, input().split())
    G = []
    for gi in range(K):
        c,d = map(int, input().split())
        G.append((gi+1,c-1,d))  # 골렘번호, 출발열, 방향
    dr = [-1,0,1,0]
    dc = [0,1,0,-1]
    A = [[0]*C for _ in range(R+2)]
    cur_gol_dict = {}
    ROW_COUNTER = 0

    for gi, c, gd in G:
        tmp_c = c
        for tmp_r in range(R+1):
            if tmp_r <= R-1:
                # down
                if A[tmp_r+2][tmp_c]==0 and A[tmp_r+1][tmp_c-1]==0 and A[tmp_r+1][tmp_c+1]==0:
                    continue
                # west
                if tmp_c > 1:
                    check_flag = True
                    for tr,tc in [(tmp_r-1,tmp_c-1),(tmp_r,tmp_c-2),(tmp_r+1,tmp_c-1),(tmp_r+1,tmp_c-2),(tmp_r+2,tmp_c-1)]:
                        if A[tr][tc] != 0:
                            check_flag = False
                            break
                    if check_flag:
                        gd = (gd-1 + 4)%4
                        tmp_c -= 1
                        continue
                # east
                if tmp_c < C-2:
                    check_flag = True
                    for tr, tc in [(tmp_r-1,tmp_c+1),(tmp_r,tmp_c+2),(tmp_r+1,tmp_c+1),(tmp_r+1,tmp_c+2),(tmp_r+2,tmp_c+1)]:
                        if A[tr][tc]!=0:
                            check_flag=False
                            break
                    if check_flag:
                        gd = (gd+1) % 4
                        tmp_c += 1
                        continue
                break   # dead end

        if tmp_r < 3:
            A = [[0]*C for _ in range(R+2)]
            cur_gol_dict = {}
            continue

        A[tmp_r][tmp_c] = gi
        for tmp_di in range(4):
            if A[tmp_r+dr[tmp_di]][tmp_c+dc[tmp_di]]!=0:
                raise Exception("우주선 겹치는 에러")
            A[tmp_r+dr[tmp_di]][tmp_c+dc[tmp_di]] = gi
        cur_gol_dict[gi] = (tmp_r,tmp_c,gd)

        # TODO -- DFS 다시 오류여지 체크
        stack = [gi]
        visit = set()
        visit.add(gi)
        max_row = 0
        while stack:
            cur_gi = stack.pop()
            center_r, center_c, gd = cur_gol_dict[cur_gi]
            if center_r == R:   # TODO "bottom-1 == R" index check
                max_row = R
                break
            exit_r, exit_c = center_r+dr[gd], center_c+dc[gd]

            dead_end_flag = True  # 지금 위치가 마지막임
            for tmp_di in range(4):
                search_r, search_c = exit_r+dr[tmp_di], exit_c+dc[tmp_di]
                if 2<=search_r<=R+1 and 0<=search_c<=C-1:
                    if A[search_r][search_c]>0 and A[search_r][search_c] not in visit:
                        new_gi = A[search_r][search_c]
                        stack.append(new_gi)
                        visit.add(new_gi)
                        dead_end_flag = False
            if dead_end_flag:
                max_row = max(max_row, center_r)
        # p(A ,tmp_r+dr[gd], tmp_c+dc[gd])
        # print("score ",max_row)
        ROW_COUNTER += max_row
        # 1 golem end
    # for end (1 golem end)
    return ROW_COUNTER

print(solution())