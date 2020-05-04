//
//  main.cpp
//  VerilogtoBench
//
//  Created by Alex Cheng on 2020/5/3.
//  Copyright © 2020 H.C C. All rights reserved.
//

#include <iostream>
#include <string>
#include <regex>
#include <vector>
#include <list>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <functional>
#include <locale>
using namespace std;

struct node{
    string node_name;
    string type;
    vector <string> fan_in_node;
    vector <string> fan_out_node;
};

class Circuit{
private:
    string name;
    unordered_map<string, node> Nodelist;
    vector <node> I_list;
    vector <node> O_list;
public:
    void SetName(string);
    /* Funtions */
    void ADD_Node(node, string);
    void VtoB();
    void Display_node();
    void Display_node_Detail();
    void Display_node_name_list();
    /* Constructor */
    Circuit();
    /* Destructor */
    ~Circuit();
    
    friend void Input_File(string, Circuit&);
    
};
void Circuit::SetName(string circuit_name){
    name = circuit_name;
}

/*Constructor & Destructor*/
Circuit::Circuit(){};
Circuit::~Circuit(){};

void Circuit::Display_node(){
    cout << name << endl;
    unordered_map<string, node>:: iterator itr;
    for (itr = Nodelist.begin(); itr != Nodelist.end(); itr++){
        cout << itr->second.node_name << " Type: " <<  itr->second.type << endl;
    }
    cout << endl;
}

void Circuit::Display_node_Detail(){
    cout << name << endl;
    unordered_map<string, node>:: iterator itr;
    for (itr = Nodelist.begin(); itr != Nodelist.end(); itr++){
        cout << itr->first << " Type: " <<  itr->second.type << endl;
        cout << "fan_in : ";
        for (int j = 0; j < itr->second.fan_in_node.size(); j++){
            cout << itr->second.fan_in_node[j] << " ";
        }
        cout << endl;
        cout << "fan_out : ";
        for (int j = 0; j < itr->second.fan_out_node.size(); j++){
            cout << itr->second.fan_out_node[j] << " ";
        }
        cout << endl;
    }
    cout << endl;
}
void Circuit::VtoB(){
    ofstream fout;
    fout.open("./result/" + name + ".bench");
    for (int i = 0; i < I_list.size(); i++){
        fout << "INPUT(" << I_list[i].node_name << ")" << endl;
    }
    fout << endl << endl;
    for (int i = 0; i < O_list.size(); i++){
        fout << "OUTPUT(" << O_list[i].node_name << ")" << endl;
    }
    fout << endl << endl;
    unordered_map<string, node>:: iterator itr;
    for (itr = Nodelist.begin(); itr != Nodelist.end(); itr++){
        if (!itr->second.fan_in_node.empty()){
            fout << itr->first << " = " << itr->second.type << "(";
            for (int j = 0; j < itr->second.fan_in_node.size(); j++){
                if (j != itr->second.fan_in_node.size()-1)
                    fout << itr->second.fan_in_node[j] << ", ";
                else
                    fout << itr->second.fan_in_node[j] << ")" << endl;
            }
        }
    }
    fout.close();
}

class Circuit_manager: public Circuit{
public:
    /* Constructor */
    Circuit_manager();
    /* Destructor */
    ~Circuit_manager();
    list <Circuit> circuit_list;
    unordered_map <string,string> circuit_info;
    
    //To be finished
};


void Input_File(string file_name, Circuit &C) {
    ifstream fin(file_name);
    string s = "";
    string eff_s = "";
    vector <string> out_name;
    if (fin.good()){
        while(getline(fin, s)){
            smatch m;
            size_t found_comment = s.find("//");
            if (found_comment == string::npos){
                size_t found = s.find(";");
                size_t found_endmodule = s.find("endmodule");
                if (found == string::npos && found_endmodule == string::npos){
                    if (eff_s == ""){
                        s.erase(std::remove(s.begin(), s.end(), '\r'), s.end());
                        eff_s = eff_s + s;
                    }
                    else{
                        s.erase(std::remove(s.begin(), s.end(), ' '), s.end());
                        s.erase(std::remove(s.begin(), s.end(), '\r'), s.end());
                        eff_s = eff_s + s;
                    }
                }
                else if (found == string::npos && found_endmodule != string::npos){
                    eff_s = eff_s + s;
                    break;
                }
                else{
                    if (eff_s == ""){
                        eff_s = eff_s + s;
                    }
                    else{
                        s.erase(std::remove(s.begin(), s.end(), ' '), s.end());
                        s.erase(std::remove(s.begin(), s.end(), '\r'), s.end());
                        eff_s = eff_s + s;
                    }
                    // Using Regex to searching information needed
                    regex input("[ ]*input (.*);");
                    regex output("[ ]*output (.*);");
                    regex gate("[ ]*([^ ]*) (.*)[ ]*[(](.*)[)];");
                    regex wire("[ ]*wire (.*);");
                    regex reg("[ ]*reg (.*);");
                    
                    if (regex_match(eff_s, m, input)){
                        cout << m[1] << endl;
                        stringstream s_stream(m[1]);
                        while(s_stream.good()) {
                            string substr;
                            getline(s_stream, substr, ','); //get first string delimited by comma
                            substr.erase(std::remove(substr.begin(), substr.end(), ' '), substr.end());
                            node ipt;
                            ipt.node_name = substr;
                            ipt.type = "IPT";
                            C.I_list.push_back(ipt);
                            C.Nodelist[ipt.node_name] = ipt;
                        }
                        
                    }
                    else if (regex_match(eff_s, m, output)){
                        cout << m[1] << endl;
                        stringstream s_stream(m[1]);
                        while(s_stream.good()) {
                            string substr;
                            getline(s_stream, substr, ','); //get first string delimited by comma
                            substr.erase(std::remove(substr.begin(), substr.end(), ' '), substr.end());
                            out_name.push_back(substr);
                        }
                    }
                    else if (regex_match(eff_s, m, gate)){
                        if (m[1] == "module"){
                            cout << m[2] << endl;
                            string name = m[2];
                            name.erase(std::remove(name.begin(), name.end(), ' '), name.end());
                            C.name = name;
                        }
                        else{
                            string out_node;
                            node g;
                            int o = 0;
                            cout << m[3] << endl;
                            stringstream s_stream(m[3]);
                            while(s_stream.good()) {
                                string substr;
                                getline(s_stream, substr, ','); //get first string delimited by comma
                                substr.erase(std::remove(substr.begin(), substr.end(), ' '), substr.end());
                                g.node_name = substr;
                                g.type = m[1];
                                //cout << substr << endl;
                                if (o == 0){
                                    vector<string>::iterator it = std::find(out_name.begin(), out_name.end(), substr);
                                    if(it != out_name.end()){
                                        C.O_list.push_back(g);
                                    }
                                    out_node = g.node_name;
                                    C.Nodelist[out_node]= g;
                                }
                                else{
                                    if (C.Nodelist.find(substr) != C.Nodelist.end()){
                                        C.Nodelist[substr].fan_out_node.push_back(out_node);
                                        C.Nodelist[out_node].fan_in_node.push_back(substr);
                                    }
                                    else{
                                        node new_node;
                                        new_node.node_name = substr;
                                        new_node.fan_out_node.push_back(out_node);
                                        C.Nodelist[out_node].fan_in_node.push_back(substr);
                                        C.Nodelist[substr] = new_node;
                                    }
                                        
                                }
                                o++;
                            }
                         }
                        
                    }
                    eff_s = "";
                }
            }
        }
             
    }
    // Close the file
    fin.close();
}



int main(int argc, const char * argv[]) {
    Circuit C;
    Input_File("c432.v",C);
    cout << endl;
    C.Display_node_Detail();
    C.VtoB();
    return 0;
}
