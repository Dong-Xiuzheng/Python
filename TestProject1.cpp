// TestProject1.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <iostream>
#include <list>
#include <deque>

using namespace std;

#define ALIGN8(T) ((sizeof(T)+7) & ~7)

template <typename T>
class objpool {
public:
	objpool(size_t max_alloc_count)
		: allocated_obj_count_(0), max_alloc_count_(max_alloc_count)
	{
		size_t alloc_size = (max_alloc_count + 1)*ALIGN8(T);
		pchunk_ = new char[alloc_size];
		memset(pchunk_, 0, alloc_size);
		
		pobj_ = reinterpret_cast<T*>(pchunk_);
		for (size_t i = 0; i < max_alloc_count_; i++) {
			new (pchunk_ + i*ALIGN8(T))T; // 在指定内存上调用构造函数
		}
	}

	~objpool() {
		delete[] pchunk_;
		pchunk_ = nullptr;
		pobj_ = nullptr;
		list_pool_.clear();
		additional_list_pool_.clear();

		///< 释放额外申请的内存
		for (auto iter = additional_cache_que_.begin(); iter != additional_cache_que_.end(); ++iter) {
			T* ptr = (*iter);
			delete ptr;
		}
		additional_cache_que_.clear();
		max_alloc_count_ = 0;
		allocated_obj_count_ = 0;
	}

	T* alloc() {
		if (allocated_obj_count_ < max_alloc_count_) {
			return &pobj_[allocated_obj_count_++];
		}
		else if (list_pool_.empty() == false){
			T* p = list_pool_.front();
			list_pool_.pop_front();
			new (p)T; // 指定内存调用构造函数
			return p;
		}

		if (additional_list_pool_.empty() == false) {
			T* p = additional_list_pool_.front();
			additional_list_pool_.pop_front();
			new (p)T; // 指定内存调用构造函数
			return p;
		}

		// 内存池已耗尽，使用新申请内存
		auto T_ptr = new T;
		additional_cache_que_.push_back(T_ptr);
		return T_ptr;
	}

	void delloc(T* p) {
		// 属于内存池内存回收
		char* upper = pchunk_ + (max_alloc_count_ + 1) * ALIGN8(T);
		if (reinterpret_cast<char*>(p) >= pchunk_ && reinterpret_cast<char*>(p) < upper) {
			list_pool_.push_front(p);
			return;
		}
		
		// 额外申请内存回收
		additional_list_pool_.push_front(p);
	}

	bool empty() {
		return allocated_obj_count_ >= max_alloc_count_;
	}

	size_t free_count() {
		return max_alloc_count_ - allocated_obj_count_;
	}

	size_t allocated_count() {
		return allocated_obj_count_;
	}

	void clear() {
		allocated_obj_count_ = 0;
		list_pool_.clear();

		for (auto iter = additional_cache_que_.begin(); iter !- additional_cache_que_.end(); ++iter) {
			T* ptr = (*iter);
			delete iter;
		}
		additional_cache_que_.clear();
		additional_list_pool_.clear();
	}

private:
	char *pchunk_;
	T* pobj_;
	size_t max_alloc_count_;
	size_t allocated_obj_count_;
	std::list<T*> list_pool_;

	std::deque<T*> additional_cache_que_;
	std::list<T*> additional_list_pool_;
};

class TestClass {
public:
	int32_t a = 0;
	int32_t b = 1;
	int8_t c = 3;
};


int main() {
    
	objpool<TestClass> test_objpool(3);

	TestClass * t1 = test_objpool.alloc();
	t1 = test_objpool.alloc();
	t1 = test_objpool.alloc();
	t1 = test_objpool.alloc();
	t1 = test_objpool.alloc();
	cout << t1->b << endl;

	return 0;
}
