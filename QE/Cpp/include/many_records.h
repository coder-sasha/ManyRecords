#pragma once

#include <cstdint>
#include <fstream>
#include <cstdlib>
#include <queue>
#include <algorithm>
#include <string>
#include <sstream>
#include <fstream>
#include <optional>
#include <chrono>
#include <cstdio>

const size_t REPORT_EVERY{ 10'000'000 };
const size_t DATA_SIZE{ 100'000'000 };

// default names of input and output files
const std::string DATA_NAME{"qe_data_1000_same.csv"};
const std::string RES_NAME{ "qe_data_1000_same_res.csv" };

// quadratic equation
struct QEP
{
	double a{ 0 }, b{ 0 }, c{ 0 };
	std::optional<float> r1;
	std::optional<float> r2;
	bool no_roots{ true };
};

// reads CSV file and solves equation
std::pair<size_t, size_t> qe_read_solve_write(std::string& data_name, std::string& res_name);
// QE solver
QEP& qe_solver(QEP& qe);
// write eqution resilts into the output file, using std::fprintf
long output_qe(QEP& dt, FILE* out_file);