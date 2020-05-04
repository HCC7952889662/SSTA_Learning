//
//  main.cpp
//  VerilogtoBench
//
//  Created by 鄭旭程 on 2020/5/3.
//  Copyright © 2020 H.C C. All rights reserved.
//

#include <iostream>
#include <string>
#include <regex>
#include <vector>
#include <list>
#include <map>
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
    map<string, node> Nodelist;
    vector <node> nodelist;
    vector <string> node_name_list;
    vector <node> I_list;
    vector <node> O_list;
public:
    void SetName(string);
    /* Funtions */
    void ADD_Node(node, string);
    void VtoB();
    void Display_node();
    void Display_node_Detail();
    /* Constructor */
    Circuit();
    /* Destructor */
    ~Circuit();
    
    friend void Input_File(string, Circuit&);
    
};
void Circuit::SetName(string circuit_name){
    name = circuit_name;
}
void Circuit::ADD_Node(node n, string type){
    if (type == "IPT"){
        I_list.push_back(n);
        nodelist.push_back(n);
        node_name_list.push_back(n.node_name);
    }
    else if (type == "OUT"){
        O_list.push_back(n);
        nodelist.push_back(n);
        node_name_list.push_back(n.node_name);
    }
    else{
        nodelist.push_back(n);
        node_name_list.push_back(n.node_name);
    }
}
/*Constructor & Destructor*/
Circuit::Circuit(){};
Circuit::~Circuit(){};

void Circuit::Display_node(){
    cout << name << endl;
    for (int i = 0; i < nodelist.size(); i++){
        cout << nodelist[i].node_name << " ";
    }
    cout << endl;
}
void Circuit::Display_node_Detail(){
    cout << name << endl;
    for (int i = 0; i < nodelist.size(); i++){
        cout << nodelist[i].node_name << " Type: " << nodelist[i].type << endl;
        cout << "fan_in : ";
        for (int j = 0; j < nodelist[i].fan_in_node.size(); j++){
            cout << nodelist[i].fan_in_node[j] << " ";
        }
        cout << endl;
        cout << "fan_out : ";
        for (int j = 0; j < nodelist[i].fan_out_node.size(); j++){
            cout << nodelist[i].fan_out_node[j] << " ";
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
    for (int i = I_list.size()+ O_list.size(); i < nodelist.size(); i++){
        fout << nodelist[i].node_name << " = " << nodelist[i].type << "(";
        for (int j = 0; j < nodelist[i].fan_in_node.size(); j++){
            if (j != nodelist[i].fan_in_node.size()-1)
                fout << nodelist[i].fan_in_node[j] << ", ";
            else
                fout << nodelist[i].fan_in_node[j] << ")" << endl;
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
    map <string,string> circuit_info;
    
    //To be finished
};


void Input_File(string file_name, Circuit &C) {
    ifstream fin(file_name);
    string s = "";
    string eff_s = "";
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
                        //cout << m[1] << endl;
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
                            C.node_name_list.push_back(ipt.node_name);
                        }
                        
                    }
                    else if (regex_match(eff_s, m, output)){
                        //cout << m[1] << endl;
                        stringstream s_stream(m[1]);
                        while(s_stream.good()) {
                            string substr;
                            getline(s_stream, substr, ','); //get first string delimited by comma
                            substr.erase(std::remove(substr.begin(), substr.end(), ' '), substr.end());
                            node out;
                            out.node_name = substr;
                            out.type = "OUT";
                            C.O_list.push_back(out);
                            C.Nodelist[out.node_name] = out;
                            C.node_name_list.push_back(out.node_name);
                            
                        }
                    }
                    else if (regex_match(eff_s, m, gate)){
                        if (m[1] == "module"){
                            //cout << m[2] << endl;
                            string name = m[2];
                            name.erase(std::remove(name.begin(), name.end(), ' '), name.end());
                            C.name = name;
                        }
                        else{
                            node g;
                            int o = 0;
                            //cout << m[3] << endl;
                            stringstream s_stream(m[3]);
                            while(s_stream.good()) {
                                string substr;
                                getline(s_stream, substr, ','); //get first string delimited by comma
                                substr.erase(std::remove(substr.begin(), substr.end(), ' '), substr.end());
                                //cout << substr << endl;
                                if (o == 0){
                                    g.node_name = substr;
                                    g.type = m[1];
                                }
                                else{
                                    g.fan_in_node.push_back(substr);
                                }
                                o++;
                            }
                            C.Nodelist[g.node_name] = g;
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
    //C.Display_node_Detail();
    C.VtoB();
    return 0;
}
