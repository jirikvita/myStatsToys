#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include <stdio.h>

// Load data from file into 2D array of strings. Input is filename and wanted numbestd::stringof columns
std::vector<std::vector<std::string> > loadDataFile(char* fileName, int cols)
{
    std::vector<std::vector<std::string> > loadedData;

    std::ifstream file (fileName);
    if(!file){
        std::cout << "File " << fileName << " not found in run directory" << std::endl;
		return loadedData;
    }

    if(file.is_open())
    {
	std::vector<std::string> row (cols);
	char c;

        while(file.get(c))
        {
            if(c != '@' && c != '#' && c != '*' && c != '$' && c != '%')
            {
                file.unget();
                for(int i = 0; i<cols; i++) // load desired columns
                {
                    file >> row[i];
                }
                loadedData.push_back(row); //store them
                file.ignore(1024,'\n'); // discard rest of line
            }
            else
              file.ignore(1024, '\n'); // discard commented lines
        }
        file.close();
    }
    return loadedData;
}

double getWeight(std::string name, std::vector<std::vector<std::string> > loadedFile)
{
	// Define file format:
	int DSID = 0;
	int fileName = 1;
	int filtEff = 2;
	int Xsection = 3;

	// Find and return appropriate filtrEff*Xsection
	int fileSize = loadedFile.size();
	for(int i = 0; i < fileSize; i++)
	{
		if(loadedFile[i][fileName].find(name) != std::string::npos)
		  return atof(loadedFile[i][filtEff].c_str())*atof(loadedFile[i][Xsection].c_str());
	}
	return -1;
}