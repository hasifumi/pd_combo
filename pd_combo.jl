# -*- coding: utf-8 -*-
# vim:set foldmethod=marker:

ROW = 5
COL = 6
MAX_TURN = 30
BEAM_WIDTH = 5000

field = zeros(Int8, ROW, COL)
f_field = zeros(Int8, ROW, COL)
chainflag = zeros(Int8, ROW, COL)
dummy = zeros(Int8, ROW, COL)
t_erace = zeros(Int8, ROW, COL)
max_count = 0
route = fill(-1, MAX_TURN, 2)

mutable struct member#={{{=#
    score::Int8
    nowR::Int8
    nowC::Int8
    prev::Int8
    movei
end#=}}}=#

function sort_member(a, b)#={{{=#
    if a.score < b.score
        return true
    end
    return false
end#=}}}=#

# sort example{{{
#    m1 = member(1, 1, 3, 4, [1 1; 2 2;])
#    m2 = member(3, 2, 3, 4, [])
#    m3 = member(2, 3, 3, 4, [])
#    arr_member = Array{member}(undef, 3)
#    arr_member[1] = m1
#    arr_member[2] = m2
#    arr_member[3] = m3
#    sort!(arr_member, lt=sort_member, rev=true)
#}}}

function set(field1=[])#={{{=#
    if field1 == []
	    for i in 1:ROW
	    	for j in 1:COL
	    		if field[i, j] == 0
	    			global field[i, j] = rand(1:6)
	    		end
	    	end
	    end
    else
        global field = copy(field1)
    end
end#=}}}=#

function show(field)#={{{=#
    for i in 1:ROW
        for j in 1:COL
            print(field[i, j])
        end
        print("\n")
    end
end#=}}}=#

function fall()#={{{=#
    for i in 1:ROW
        for j in 1:COL
            for k in 1:ROW
                if k+1 > ROW
                    break
                end
                if field[k+1, j] == 0
                    global field[k+1, j] = field[k, j]
                    global field[k, j] = 0
                end
            end
        end
    end
end#=}}}=#

function swap(i1, j1, i2, j2)#={{{=#
    temp = field[i1, j1]
    global field[i1, j1] = field[i2, j2]
    global field[i2, j2] = temp
end#=}}}=#

function operation()#={{{=#
    now_col = route[1, 1]
    now_row = route[1, 2]
    #print("now_col" , now_col , ", now_row:" , now_row, "\n")

    for i in 1:MAX_TURN
        if route[i, 1] == -1 || route[i, 2] == -1
            break
        end
        swap(now_col, now_row, route[i, 2], route[i, 1])
        now_col = route[i, 2]  # x position
        now_row = route[i, 1]  # y position
    end
end#=}}}=#

function chain(now_row, now_col, drop, count)#={{{=#
    if now_row == 0 || now_row > ROW || now_col == 0 || now_col > COL
        return
    end
    if field[now_row, now_col] == drop && chainflag[now_row, now_col] == 0
        global chainflag[now_row, now_col] = -1
        if max_count < count
            global max_count = count
        end
        global dummy[now_row, now_col] = -1

        chain(now_row-1, now_col, drop, count+1)
        chain(now_row+1, now_col, drop, count+1)
        chain(now_row, now_col-1, drop, count+1)
        chain(now_row, now_col+1, drop, count+1)
    end
end#=}}}=#

function evaluate()#={{{=#
    value = 0
    chainflag = zeros(Int8, ROW, COL)
    for i in 1:ROW
        for j in 1:COL
            if chainflag[i, j] == 0 && field[i, j] != 0
                global max_count = 0
                global dummy = zeros(Int8, ROW, COL)
                chain(i, j, field[i, j], 1)
                if max_count >= 3
                    if check() == 1
                        value += 1
                    end
                end
            end
        end
    end
    return value
end#=}}}=#

function check()#={{{=#
    v = 0
    for i in 1:ROW
        for j in 1:COL-2
            if dummy[i, j] == -1 && dummy[i, j+1] == -1 && dummy[i, j+2] == -1 && field[i, j] == field[i, j+1] && field[i, j] == field[i, j+2]
                global t_erace[i, j] = -1
                global t_erace[i, j+1] = -1
                global t_erace[i, j+2] = -1
                v = 1
            end
        end
    end

    for i in 1:ROW-2
        for j in 1:COL
            if dummy[i, j] == -1 && dummy[i+1, j] == -1 && dummy[i+2, j] == -1 && field[i, j] == field[i+1, j] && field[i, j] == field[i+2, j]
                global t_erace[i, j] = -1
                global t_erace[i+1, j] = -1
                global t_erace[i+2, j] = -1
                v = 1
            end
        end
    end
    return v
end#=}}}=#

function sum_e()#={{{=#
    combo = 0
    while(1==1)
        global t_erace = zeros(Int8, ROW, COL)
        a = evaluate()
        if a == 0
            break
        end
        for i in 1:ROW
            for j in 1:COL
                if t_erace[i, j] == -1
                    global field[i, j] = 0
                end
            end
        end
        fall()
        combo += a
    end
    return combo
end#=}}}=#

function main()#={{{=#
	set()
    #set([1 1 1 1 1 1; 2 2 2 2 2 2; 3 3 3 3 3 3; 4 4 4 4 4 4; 5 5 5 5 5 5;])
    println("initial field.")
    show(field)
    f_field = copy(field)
    route[1:6 , : ] = [1 1; 2 1; 3 1; 4 1; 5 1; 6 1;]
    print(route[1:6, :], "\n")
    operation()
    println("after operation")
    show(field)
    combo = sum_e()
    println("combo:", combo)
    println("after sum_e")
    show(field)

    #fall()
    #swap(1, 1, 2, 1)
    #println("after swap")
    #show(field)
end#=}}}=#

main()

