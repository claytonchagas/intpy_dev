import ast

def python_code_to_AST(file_name):
    try:
        #Opening file
        file = open(file_name, "r")

    except:
        print("Error while trying to open file!")
        print("Check if the file exists!")
        return None

    else:
        try:
            #Generating AST from Python code
            return ast.parse(file.read())

        except:
            print("Error while trying to generate AST from the Python code!")
            print("Check if your Python script is correctly writen.")
            return None

class FunctionClassMethodSearcher(ast.NodeVisitor):
    def __init__(self, AST):
        self.__AST = AST
        self.__imported_modules = []
        self.__functions = {}

        """
        self.__classes = []
        self.__instance_methods = {}
        self.__class_methods = {}

        self.__super_functions = []
        self.__super_classes = []
        self.__super_methods = []
        """

    def search_for_functions_classes_and_methods(self):
        #Finding all declared functions in the AST
        """
        self.__current_class = None
        self.__current_class_name = ""
        """

        self.__current_function = None
        self.__current_function_name = ""
        self.visit(self.__AST)

    def visit_Import(self, node):
        if(node not in self.__imported_modules):
            self.__imported_modules.append(node)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if(node not in self.__imported_modules):
            self.__imported_modules.append(node)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        #This function avoids that child nodes of ClassDef nodes
        #(ex.: methods) be visited during search
        """
        previous_class_name = self.__current_class_name
        if(self.__current_class_name == ""):
            self.__current_class_name = node.name
        else:
            self.__current_class_name = self.__current_class_name + "." + node.name
        
        previous_class = self.__current_class
        self.__current_class = node
        
        #Adding new class found to "self.__classes"
        self.__classes.append(node)

        for son_node in node.body:
            
            #Checking if "node" is a superclass
            if isinstance(son_node, ast.ClassDef):
                self.__super_classes.append(node)
                break
            
            
            if(isinstance(son_node, ast.FunctionDef)):
                
                #Checking if "son_node" is a supermethod
                for element in son_node.body:
                    if(isinstance(element, ast.FunctionDef)):
                        self.__super_methods.append(son_node)
                        break
                

                #Checking if "son_node" is an instance method or a class method
                is_a_class_method = False
                for decorator in son_node.decorator_list:
                    if(decorator.id == "staticmethod"):
                        is_a_class_method = True
                        break
                
                method_name = self.__current_class_name + "." + son_node.name
                if(is_a_class_method):
                    self.__class_methods[method_name] = son_node
                else:
                    self.__instance_methods[method_name] = son_node
        
        self.generic_visit(node)

        self.__current_class = previous_class
        self.__current_class_name = previous_class_name
        """
    
    def visit_FunctionDef(self, node):
        previous_function_name = self.__current_function_name
        if(self.__current_function_name == ""):
            self.__current_function_name = node.name
        else:
            self.__current_function_name = self.__current_function_name + "." + node.name
        
        previous_function = self.__current_function
        self.__current_function = node

        """
        if(self.__current_class == None) or ((node not in self.__instance_methods.values()) and (node not in self.class_methods.values())):
            #Adding new function found to "self.__functions"
            function_name = ""
            if(self.__current_class_name != ""):
                function_name = self.__current_class_name + "." + self.__current_function_name
            else:
                function_name = self.__current_function_name
        """
        self.__functions[self.__current_function_name] = node

        """
            #Checking if "node" is a superfunction
            for son_node in node.body:
                if isinstance(son_node, ast.FunctionDef):
                    self.__super_functions.append(node)
                    break
        """

        self.generic_visit(node)

        self.__current_function = previous_function
        self.__current_function_name = previous_function_name

    @property
    def imported_modules(self):
        return self.__imported_modules

    @property
    def functions(self):
        return self.__functions

    """
    @property
    def classes(self):
        return self.__classes
    
    @property
    def instance_methods(self):
        return self.__instance_methods

    @property
    def class_methods(self):
        return self.__class_methods
    
    @property
    def super_functions(self):
        return self.__super_functions

    @property
    def super_classes(self):
        return self.__super_classes  

    @property
    def super_methods(self):
        return self.__super_methods
    """

class FunctionGraphCreator(ast.NodeVisitor):
    """
    def __init__(self, AST, functions, class_methods, instance_methods):
        #The "AST" argument passed to this constructor must be the AST of the Python code
        #The arguments "functions", "class_methods" and "instance_methods" must be dictionaries
        #which keys must be strings representing the name of the functions/methods and the
        #values must be the correspondents AST nodes
    """
    def __init__(self, AST, functions):
        #The "AST" argument passed to this constructor must be the AST of the Python code
        #The argument "functions" must be a dictionary which keys must be strings representing
        #the name of the functions and the values must be the correspondents AST nodes

        self.__AST = AST
        self.__functions = functions
        """
        self.__class_methods = class_methods
        self.__instance_methods = instance_methods
        """

        self.__function_graph = Graph()

    def generate_function_graph(self):
        #Inserting all functions in the function graph
        for function in self.__functions.values():
            self.__function_graph.insert_vertice(GraphVertice(function))
        
        """
        for class_method in self.__class_methods.values():
            self.__function_graph.insert_vertice(GraphVertice(class_method))

        for instance_method in self.__instance_methods.values():
            self.__function_graph.insert_vertice(GraphVertice(instance_method))

        self.__current_class_name = ""
        """

        self.__current_function_name = ""
        self.__current_function = None
        self.visit(self.__AST)

    def visit_ClassDef(self, node):
        #This function avoids that child nodes of ClassDef nodes
        #(ex.: methods) be visited during the graph creation
        """
        previous_class_name = self.__current_class_name
        if(self.__current_class_name != ""):
            self.__current_class_name = self.__current_class_name + "." + node.name
        else:
            self.__current_class_name = node.name

        self.generic_visit(node)

        self.__current_class_name = previous_class_name
        """

    def visit_FunctionDef(self, node):
        previous_function_name = self.__current_function_name
        if(self.__current_function_name != ""):
            self.__current_function_name = self.__current_function_name + "." + node.name
        else:
            self.__current_function_name = node.name
        
        previous_function = self.__current_function
        self.__current_function = node

        self.generic_visit(node)

        self.__current_function_name = previous_function_name
        self.__current_function = previous_function

    def visit_Call(self, node):
        #Testing if this node represents a call to some function done inside another function
        if(self.__current_function_name != ""):
            function_called = None
            
            if(isinstance(node.func, ast.Name)):
                #In this case the function called can be either a function imported from a module
                #or a function declared by the user in the file

                function_called_name = node.func.id
                
                #Finding possible functions (declared by the user) being called
                possible_functions_called = []
                for function_name in self.__functions:
                    if(function_name.split(".")[-1] == function_called_name):
                        possible_functions_called.append(function_name)

                if(len(possible_functions_called) >= 1):
                    #Finding function defined in the smaller scope
                    """
                    function_called_name_prefix = ""
                    
                    if(self.__current_class_name != ""):
                        function_called_name_prefix = self.__current_class_name + "." + self.__current_function_name + "."
                    else:
                    """
                    function_called_name_prefix = self.__current_function_name + "."
                    
                    while(function_called == None):

                        for possible_function_called in possible_functions_called:
                            if(function_called_name_prefix + function_called_name == possible_function_called):
                                function_called = self.__functions[possible_function_called]
                                break
                        
                        if(function_called_name_prefix == ""):
                            break

                        #The string in "function_called_name_prefix" always ends in a dot (".")
                        #Hence, the last element of "function_called_name_prefix.split('.')" will
                        #always be a blank string ("")
                        if(len(function_called_name_prefix.split(".")) > 2):
                            function_called_name_prefix = function_called_name_prefix.split(".")
                            function_called_name_prefix.pop(-2)
                            function_called_name_prefix = ".".join(function_called_name_prefix)
                        else:
                            function_called_name_prefix = ""
                        
                        """
                        if(self.__current_class_name != ""):
                            #Testing if (function_called_name_prefix = self.__current_class_name + ".")
                            #In this case function_called_name_prefix must be an empty string because
                            #to call a method of a class it is necessary to use the strucutre
                            #self.instance_method() or ClassName.class_method() and in both cases node.func
                            #is not an instance of ast.Name
                            if(len(function_called_name_prefix) == len(self.__current_class_name) + 1 ):
                                function_called_name_prefix = ""
                        """
            """
            elif(isinstance(node.func, ast.Attribute)):
                #In this case the function called is a function imported from a module

                #Building the name of the function called
                current_node = node.func
                function_called_name_parts = []
                while(isinstance(current_node, ast.Attribute)):
                    function_called_name_parts.append(current_node.attr)
                    current_node = current_node.value
                function_called_name_parts.append(current_node.id)

                function_called_name_parts.reverse()
                function_called_name = ".".join(function_called_name_parts)
                
                
                #Testing if the function called is an instance method
                if(function_called_name[0] == "self"):
                    #Removing "self." from the name of the instance method
                    function_called_name = ".".join(function_called_name_parts[1:])
                    
                    for instance_method_name in self.__instance_methods:
                        if(self.__current_class_name + "." + function_called_name == instance_method_name):
                            function_called = self.__instance_methods[instance_method_name]
                            break
                else:
                    #In this case, the function called is a class method
                    for class_method_name in self.__class_methods:
                        if(function_called_name == class_method_name):
                            function_called = self.__class_methods[class_method_name]
                            break
            """

            #Testing if the function called is one of the functions declared by the user
            if(function_called != None):
                #Inserting "function_called" in function graph
                function_called_graph_vertice = self.__function_graph.search_vertice(function_called)
                current_function_graph_vertice = self.__function_graph.search_vertice(self.__current_function)
                
                ##############CHECK IF THIS CONDITIONAL IS NECESSARY
                if(function_called_graph_vertice == None or current_function_graph_vertice == None):
                    raise RuntimeError("Internal error!")
                else:
                    current_function_graph_vertice.insert_link(function_called_graph_vertice)
        
        self.generic_visit(node)
    
    @property
    def function_graph(self):
        return self.__function_graph

class Graph():
    def __init__(self):
        #Each element of self.__vertices should be of type GraphVertice
        self.__vertices = []

    def insert_vertice(self, vertice):
        if(vertice not in self.__vertices):
            self.__vertices.append(vertice)

    #Returns the vertice which value of the attribute "data" is equals to the
    #argument "data" passed to this method.
    #If none of the vertices matches, returns None
    def search_vertice(self, data):
        for vertice in self.__vertices:
            if(vertice.data == data):
                return vertice
        return None

    @property
    def vertices(self):
        return self.__vertices

    ############DEBUG#############
    def print_graph(self, d):
        for vertice in self.__vertices:
            vertice.print_graph_vertice(d)

class GraphVertice():
    def __init__(self, data):
        self.__data = data

        #The elements of self.__linked_vertices should be of type GraphVertice
        self.__linked_vertices = []

    #Insert "link" in "self.__linked_vertices"
    def insert_link(self, link):
        if(link not in self.__linked_vertices):
            self.__linked_vertices.append(link)

    @property
    def data(self):
        return self.__data

    @property
    def linked_vertices(self):
        return self.__linked_vertices

    ##########DEBUG#############
    def print_graph_vertice(self, d):
        for e in d:
            if(self.data == d[e]):
                print("Graph Vertice:", e)
        for linked_vertice in self.__linked_vertices:
            for e in d:
                if(linked_vertice.__data == d[e]):
                    print("    Linked Vertice:", e)

def get_source_code_executed(function, function_graph):
    list_of_graph_vertices_not_yet_processed = []
    list_of_graph_vertices_already_processed = []
    source_codes_executed = []

    for graph_vertice in function_graph.vertices:
        current_function_def_node = graph_vertice.data
        if(current_function_def_node.name == function.__name__):
            list_of_graph_vertices_not_yet_processed.append(graph_vertice)

    while(len(list_of_graph_vertices_not_yet_processed) > 0):
        current_vertice = list_of_graph_vertices_not_yet_processed.pop(0)

        source_codes_executed.append(ast.unparse(current_vertice.data))

        for linked_vertice in current_vertice.linked_vertices:
            if(linked_vertice not in list_of_graph_vertices_not_yet_processed and
            linked_vertice not in list_of_graph_vertices_already_processed and
            linked_vertice != current_vertice):
                list_of_graph_vertices_not_yet_processed.append(linked_vertice)
        
        list_of_graph_vertices_already_processed.append(current_vertice)
    
    return "\n".join(source_codes_executed)
