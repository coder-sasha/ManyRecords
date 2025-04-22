// 2024
// The Project ManyRecords. C++ solution
// MR-QE-Parallel.cpp: read it all and solve with std::parallel
//

// needed to compile csv.h
#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <algorithm>
#include <cmath>
#include <execution>  // Required for parallel execution

#include "many_records.h"
#include "csv.h"

std::vector<QEP>& qe_read_into_vec(std::string& data_name, std::vector<QEP>& qe_data)
{
	io::CSVReader<3> in(data_name);
	QEP qep;

	in.read_header(io::ignore_extra_column, "a", "b", "c");
	while (in.read_row(qep.a, qep.b, qep.c))
	{
		qe_data.emplace_back(qep);

		if (qe_data.size() % REPORT_EVERY == 0)
			std::cout << " loaded " << qe_data.size() << "\n";
	}

	return qe_data;
}

void qe_solve(QEP& qe)
{
	qe.no_roots = true;
	qe.r1 = qe.r1= std::nullopt;

	if (qe.a != 0)
	{
		auto a2 = qe.a * 2;
		auto d = (qe.b * qe.b) - (2 * a2 * qe.c);
		if (d >= 0)
		{
			auto sqrt_disc = std::sqrt(d);
			if (d > 0)
			{
				qe.r1 = (-qe.b + sqrt_disc) / a2;
				qe.r2 = (-qe.b - sqrt_disc) / a2;
			}
			else
				qe.r1 = (-qe.b / a2);
			qe.no_roots = false;
		}
	}
	else
		if (qe.c)
		{
			qe.r1 = (-qe.b / qe.c);
			qe.no_roots = false;
		}
}

int save_results(std::vector<QEP>& qe_data, std::string& res_name)
{
	int ret{ 42 };
	size_t no_roots{ 0 };
	FILE* out_file = fopen(res_name.c_str(), "w");

	if (!out_file)
	{
		std::cerr << "Failed to open the output file " << res_name << std::endl;
		return ret;
	}
	else
		// write reasult header
		std::fprintf(out_file, "%s\n", "a, b, c, r1, r2");

	for (const auto& dt : qe_data)
	{
		std::fprintf(out_file, "%f,%f,%f,", dt.a, dt.b, dt.c);

		if (dt.no_roots)
		{
			++no_roots;
			std::fprintf(out_file, "%s\n", "None, None");
		}
		else
		{
			if (dt.r1.has_value())
				std::fprintf(out_file, "%f,", *dt.r1);
			else
				std::fprintf(out_file, "%s,", "None");

			if (dt.r2.has_value())
				std::fprintf(out_file, "%f\n", *dt.r2);
			else
				std::fprintf(out_file, "%s\n", "None");
		}
	}
	fclose(out_file);
	std::cout << qe_data.size() << " saved. " << no_roots << " without roots\n";
	ret = 0;

	return ret;
}

int main(int argc, char** argv)
{
	int ret{ 42 };
	std::string data_name{ DATA_NAME };
	std::string res_name{ RES_NAME };
	std::vector<QEP> qe_data;

	if (argc > 1)
	{
		data_name = argv[1];
		if (argc > 2)
			res_name = argv[2];
	}

	qe_data.reserve(DATA_SIZE);
	// measure the execution timing
	using std::chrono::duration_cast;
	using std::chrono::microseconds;
	using std::chrono::milliseconds;
	using std::chrono::steady_clock;

	auto start = steady_clock::now();
	std::cout << "Solving QEs STL Parallel Processing\n";

	auto finish = steady_clock::now();
	auto duration_ms = duration_cast<milliseconds>(finish - start).count();
	auto duration_us = duration_cast<microseconds>(finish - start).count();

	try
	{
		qe_data = qe_read_into_vec(data_name, qe_data);
		std::cout << qe_data.size() << " equations. Reading time: ";
		if (duration_ms < 1)
			std::cout << duration_us << "µs\n";
		else
		{
			std::cout << (duration_ms > 1000.0 ? (duration_ms / 1000.0) : duration_ms) << "ms\n";
		}

		std::cout << "Start solving...\n";
		std::for_each(std::execution::par, qe_data.begin(), qe_data.end(), qe_solve);

		finish = steady_clock::now();
		duration_ms = duration_cast<milliseconds>(finish - start).count();
		duration_us = duration_cast<microseconds>(finish - start).count();

		std::cout << "CPU time: ";
		if (duration_ms < 1)
			std::cout << duration_us << "µs\n";
		else
			std::cout << duration_ms << "ms\n";


	}
	catch (const std::exception& ex)
	{
		std::cerr << "Failed to read and solve from " << data_name << "!\t" << ex.what() << std::endl;
		return ret;
	}

	std::cout << "Savign Results\n";
	ret = save_results(qe_data, res_name);
	finish = steady_clock::now();
	duration_ms = duration_cast<milliseconds>(finish - start).count();
	duration_us = duration_cast<microseconds>(finish - start).count();

	std::cout << "ret=" << ret << "\tTotal running time : ";
	if (duration_ms < 1)
		std::cout << duration_us << "µs\n";
	else
		std::cout << (duration_ms > 1000.0 ? (duration_ms / 1000.0) : duration_ms) << "ms\n";

	return ret;
}
/*
PS C:\aWork\CppBin\Cpp1BRows\mr_cpp\QE\MR-QE\x64\Debug> .\MR-QE-Parallel.exe data_100_000_000.csv
Solving QEs STL Parallel Processing
 loaded 10000000
 loaded 20000000
 loaded 30000000
 loaded 40000000
 loaded 50000000
 loaded 60000000
 loaded 70000000
 loaded 80000000
 loaded 90000000
99999999 equations. Reading time: 206us
Start solving...
CPU time: 44.425ms
Savign Results
99999999 saved. 35149120 without roots
ret=0   Total running time : 377.105ms
*/
