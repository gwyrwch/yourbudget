#include <iostream>
#include <vector>
#include <string>
#include <assert.h>
#include <deque>
#include <algorithm>
#include <fstream>

using namespace std;

 /*
 Parameters: string
 <img src="assets/img/logo.png" alt="">
 Return value:
 <img src="{% static "assets/img/logo.png" %}" alt="">
 */

vector<string> convert(const vector<string>& html) {

	vector<string> res;
	for (auto line : html) {
		for (int i = 0; i + 8 <= line.size(); i++) {
			if (line.substr(i, 8) == "\"assets/") {
				int j = i + 1;
				while (line[j] != '"')
					j++;
				j++;
				line.insert(j, " %}\"");
				line.insert(i, "\"{% static ");
				i += 11;
			}
		}
		res.push_back(line);
	}

	return res;
}

void convert(const string& path) {
	ifstream cin(path);
	vector<string> html;
	string line;

	while (getline(cin, line))
		html.push_back(line);
	cin.close();

	html = convert(html);

	ofstream cout(path);
	for (auto e : html)
		cout << e << "\n";
}

int main() {
	ios_base::sync_with_stdio(0);

	convert("index.html");
	return 0;
}