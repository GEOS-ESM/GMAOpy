#include "Python.h"
#include "arrayobject.h"

PyDoc_STRVAR(read__doc__,
		"gridded observation utility");

static PyObject * hello(PyObject *self, PyObject *args)
{
    printf(self);
	Py_RETURN_NONE;
}

static PyObject* exception(PyObject *self, PyObject *args)
{
    PyErr_Format(PyExc_IOError,"gridded_obs: %s","this should be an exception");
    return NULL;
}

static PyMethodDef griddded_obs_methods[] = {

	{"hello",  hello, METH_VARARGS, read__doc__},
	{"exception",  exception, METH_VARARGS, read__doc__},
	{NULL, NULL}      /* sentinel */
};

PyMODINIT_FUNC init_gridded_obs(void)
{
	PyObject* m;
	m = Py_InitModule3("_obs_gridder", griddded_obs_methods, NULL); 
	import_array();  // Must be present for NumPy.  Called first after above line.
}
