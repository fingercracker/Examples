#include "system_file.h"

int some_func(int x);

#ifdef SYSTEM_SUCCESSFUL
typedef system_type fsw_type;
#define SUCCESSFUL SYSTEM_SUCCESSFUL
#endif

#ifdef SYSTEM_INTERNAL_ERROR
#define INTERNAL_ERROR SYSTEM_INTERNAL_ERROR
#endif
