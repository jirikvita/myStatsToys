// jk 17.11.2022


#include "TMath.h"
#include "TString.h"

#include <iostream>
#include <string>
#include <sstream>

// not a very nice C include for itoa and ftoa functions:
// #include <stdlib.h>


using std::string;
using std::to_string;

using std::cout;
using std::cerr;
using std::endl;

void strings()

{


  int i = 5;
  float a = TMath::TwoPi();

  // 0) the heavy weight solution: using the C++ string stream!;-)
  // cout-like syntax:
  ostringstream mysstream; 
  string strtmp = "";
  mysstream << strtmp << "some int is " << i << " while some float is " << a;
  string str0 = mysstream.str();
  cout << str0 << endl;
  
  // 1)
  string str1 = "some int is " + to_string(i) + " while some float is " + to_string(a);
  // the C++ string has the method c_str() which returns its content as the const char
  // it is not needed in cout, but useful for passing strings to function arguments
  cout << str1.c_str() << endl;

  // 2) C solution, doesn'r work for me...
  // https://stackoverflow.com/questions/190229/where-is-the-itoa-function-in-linux
  // using stricly C int-to a literal functions and float to a literal functions:
  // not available in general?
  // string str2 = "some int is " + itoa(i) + " while some float is " + ftoa(a);
  // cout << str2.c_str() << endl;

  
  // 3)
  // https://root.cern.ch/doc/master/classTString.html
  // Form is a method coming with TString
  // it uses a C-like printf-like syntax and offers formatting of floats
  TString str3 = Form("some int is %i while some float is %1.4f", i, a);
  cout << str3.Data() << endl;

  // 3.5) like 2) but with ROOT's TString functions;)
  // using stricly C int-to a literal functions and float to a literal functions:
  // Itoa needs a base argument
  TString str3p5 = "some int is " + TString::Itoa(i, 10) + " while some float is " + Form("%f", a); // there does not seem to be Ftoa(a) ...
  cout << str3p5.Data() << endl;
  
  
  // 4) using TString operators between TString and int and float 
  TString str4 = "some int is ";
  str4 += i;
  str4 += " while some float is ";
  str4 += a;
  cout << str4.Data() << endl;
  

}
