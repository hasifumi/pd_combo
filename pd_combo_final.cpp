#include <windows.h>
#include <vector>
#include <cfloat>
#include <cstdio>
#include <cstring>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include <string>
#include <iostream>
#include <cstdint>
#include <algorithm>
#include <cassert>
#include <random>
#include <queue>
#include <list>
#include <map>
#include <array>
#include <chrono>
#include <fstream>
#include <functional>

using namespace std;

#define ROW 5
#define COL 6
#define MAX_TURN 70
#define BEAM_WIDTH 5000

void init();

void fall();

void set();

void show_field();

unsigned int rnd(int mini, int maxi);

double d_rnd(double mini, double maxi);

int field[ROW][COL];

int max_count;

int chainflag[ROW][COL];

int dummy[ROW][COL];

void chain(int now_row, int now_col, int d, int count);

int evaluate();

int t_erase[ROW][COL];

int check();

int sum_evaluate();

int sum_e();

int route[100][2];

void operation();

int f_field[ROW][COL];

struct member {
	int movei[100][2];
	int score;
	int nowC;
	int nowR;
	int prev;
	member() {
		this->score = 0;
		this->prev = -1;
		memset(this->movei, -1, sizeof(this->movei));
	}
	bool operator < (const member &n)const {
		return score < n.score;
	}
}temp;


struct Action {
	int score;
	int moving[100][2];
	Action() {
		this->score = 0;
		memset(this->moving, -1, sizeof(this->moving));
	}
};

Action BEAM_SEARCH();

Action BEAM_SEARCH(){
	queue<member>que;

	for (int i = 0; i < ROW; i++) {
		for (int j = 0; j < COL; j++) {
			member cand;
			cand.nowC = j;
			cand.nowR = i;
			cand.prev = -1;
			memset(cand.movei, -1, sizeof(cand.movei));
			cand.movei[0][1]=j;
			cand.movei[0][0]=i;
			que.push(cand);
		}
	}

	int dx[4] = { -1,0,0,1 };
	int dy[4] = { 0,-1,1,0 };

	Action bestAction;
	int maxValue = 0;

	for (int i = 1; i < MAX_TURN; i++) {

		priority_queue<member, vector<member>, less<member> >pque;

		while (!que.empty()) {
			temp = que.front(); que.pop();
			for (int j = 0; j < 4; j++) {
				memcpy(field, f_field, sizeof(f_field));
				member cand = temp;
				if (0 <= cand.nowC + dx[j] && cand.nowC + dx[j] < COL && 0 <= cand.nowR + dy[j] && cand.nowR + dy[j] < ROW) {
					if (cand.prev + j == 3) {
						continue;
					}
					cand.nowC += dx[j];
					cand.nowR += dy[j];
					cand.movei[i][0] = cand.nowR;
					cand.movei[i][1] = cand.nowC;
					memcpy(route, cand.movei, sizeof(cand.movei));
					operation();
					cand.score = sum_e();
					cand.prev = j;
					pque.push(cand);
				}
			}
		}
		for (int j = 0; j < BEAM_WIDTH && !pque.empty(); j++) {
			temp = pque.top(); pque.pop();
			if (maxValue < temp.score) {
				maxValue = temp.score;
				bestAction.score = maxValue;
				for (int m = 0; m < MAX_TURN; m++) {
					bestAction.moving[m][0] = temp.movei[m][0];
					bestAction.moving[m][1] = temp.movei[m][1];
				}
			}
			if (i < MAX_TURN-1) {
				que.push(temp);
			}
		}
	}
	return bestAction;
}

void show_field(){
	int i,j;
	for(i=0;i<ROW;i++){
		for(j=0;j<COL;j++){
			printf("%d",field[i][j]);
		}
		printf("\n");
	}
}


void fall(){
	int i,j;

	for(i=ROW-1;i>=0;i--){
		for(j=0;j<COL;j++){
			int check=i;
			while(1){
				if(check==ROW-1){break;}
				if(field[check+1][j]==0){
					field[check+1][j]=field[check][j];
					field[check][j]=0;
				}
				check++;
			}
		}
	}
}

void init(){
	int i,j;

	for(i=0;i<ROW;i++){
		for(j=0;j<COL;j++){
			field[i][j]=rnd(0,6);
		}
	}
}
void set(){
	int i,j;

	for(i=0;i<ROW;i++){
		for(j=0;j<COL;j++){
			if(field[i][j]==0){
				field[i][j]=rnd(1,6);
			}
		}
	}
}

void chain(int now_row, int now_col, int d, int count) {

	if (now_row == -1 || now_row == ROW || now_col == -1 || now_col == COL) { return; }

	if (field[now_row][now_col] == d && chainflag[now_row][now_col] == 0) {

		chainflag[now_row][now_col] = -1;
		if (max_count < count) { max_count = count; }
		dummy[now_row][now_col] = -1;

		chain(now_row - 1, now_col, d, count + 1);
		chain(now_row + 1, now_col, d, count + 1);
		chain(now_row, now_col - 1, d, count + 1);
		chain(now_row, now_col + 1, d, count + 1);
	}

}
int evaluate() {

	int value = 0;
	int col_1 = COL - 1;
	int flg_row;
        // printf("col_1:%d\n", col_1);

	memset(chainflag, 0, sizeof(chainflag));

	for (int row = 0; row < ROW; row++) {
		flg_row = 0;
		for (int col = 0; col < COL; col++) {
			if (chainflag[row][col] == 0 && field[row][col] != 0) {
				max_count = 0;
				memset(dummy, 0, sizeof(dummy));
				chain(row, col, field[row][col], 1);
				if (max_count >= 3) {
					if (check() == 1) { value++; }
				}
			}
			if ( col < col_1 ) {
				if ( field[row][col] != 0 && field[row][col] == field[row][col+1]) {
					flg_row++;
				}
			}
		}
		if ( flg_row == col_1 ) {
			// printf("flg_row:%d\n",flg_row);
			// printf("col_1:%d\n",col_1);
			value += 10;
		        // printf("value add 10.\n");
			// show_field();
		}
	}

	return value;
}

int sum_evaluate() {

	int a;
	int combo = 0;

	while (1) {

		memset(t_erase, 0, sizeof(t_erase));
		a = evaluate();

		if (a == 0) { break; }

		for (int row = 0; row < ROW; row++) {
			for (int col = 0; col < COL; col++) {
				if (t_erase[row][col] == -1) { field[row][col] = 0; }
			}
		}

		fall();
		set();

		combo += a;

	}
	return combo;

}
int sum_e() {

	int a;
	int combo = 0;

	while (1) {

		memset(t_erase, 0, sizeof(t_erase));
		a = evaluate();

		if (a == 0) { break; }

		for (int row = 0; row < ROW; row++) {
			for (int col = 0; col < COL; col++) {
				if (t_erase[row][col] == -1) { field[row][col] = 0; }
			}
		}

		fall();
		combo += a;

	}
	return combo;

}


int check() {

	int v = 0;
	for (int row = 0; row < ROW; row++) {
		for (int col = 0; col < COL - 2; col++) {
			if (dummy[row][col] == -1 && dummy[row][col + 1] == -1 &&
				dummy[row][col + 2] == -1 && field[row][col] == field[row][col + 1] &&
				field[row][col] == field[row][col + 2]) {
					t_erase[row][col] = -1;
					t_erase[row][col + 1] = -1;
					t_erase[row][col + 2] = -1;
					v = 1;
			}

		}

	}
	for (int col = 0; col < COL; col++) {
		for (int row = 0; row < ROW - 2; row++) {
			if (dummy[row][col] == -1 && dummy[row + 1][col] == -1 &&
				dummy[row + 2][col] == -1 && field[row][col] == field[row + 1][col] &&
				field[row][col] == field[row + 2][col]) {
					t_erase[row][col] = -1;
					t_erase[row + 1][col] = -1;
					t_erase[row + 2][col] = -1;
					v = 1;
			}

		}

	}
	return v;
}

void operation() {

	int now_col=route[0][1];
	int now_row=route[0][0];

	int i;

	for(i=1;i<MAX_TURN;i++){
		if(route[i][0]==-1||route[i][1]==-1){break;}
		swap(field[now_row][now_col], field[route[i][0]][route[i][1]]);
		now_col=route[i][1];
		now_row=route[i][0];

	}

}
unsigned int rnd(int mini, int maxi) {
	static unsigned int x = 123456789;
	static unsigned int y = 362436069;
	static unsigned int z = 521288629;
	static unsigned int w = time(NULL) % INT_MAX;
	unsigned int t;

	t = x ^ (x << 11);
	x = y; y = z; z = w;
	w = (w ^ (w >> 19)) ^ (t ^ (t >> 8));

	return (w / (UINT_MAX / ((maxi - mini) + 1))) + mini;

}
double d_rnd(double mini, double maxi) {
	static unsigned int x = 123456789;
	static unsigned int y = 362436069;
	static unsigned int z = 521288629;
	static unsigned int w = time(NULL) % INT_MAX;
	unsigned int t;

	t = x ^ (x << 11);
	x = y; y = z; z = w;
	w = (w ^ (w >> 19)) ^ (t ^ (t >> 8));

	return (((double)w / ((double)UINT_MAX + 1)) * (maxi - mini)) + mini;

}

int main() {

	int i,j;

	double avg=0;

	int repeat_time = 1;

	for(i=0; i<repeat_time; i++){
		init();
		set();
		printf("initial field\n");
		show_field();
		memcpy(f_field,field,sizeof(field));
		Action tmp=BEAM_SEARCH();
		memcpy(route,tmp.moving,sizeof(tmp.moving));
		// printf("(x,y)=(%d,%d)\n",route[0][1],route[0][0]);
		// for(j=1;j<MAX_TURN;j++){
		// 	if(route[j][1]==-1||route[j][0]==-1){break;}
		// 	if(route[j][1]==route[j-1][1]+1){printf("RIGHT");}
		// 	if(route[j][1]==route[j-1][1]-1){printf("LEFT");}
		// 	if(route[j][0]==route[j-1][0]+1){printf("DOWN");}
		// 	if(route[j][0]==route[j-1][0]-1){printf("UP");}
		// 	printf("\n");
		// }
		memcpy(field,f_field,sizeof(f_field));
		operation();
		printf("operated field\n");
		show_field();
		int combo=sum_e();
		printf("%dコンボ\n",combo);
		avg+=(double)combo;
	}

	printf("平均コンボ数:%lf\n",avg/repeat_time);

	return 0;
}
