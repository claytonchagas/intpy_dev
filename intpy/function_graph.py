import ast, os, os.path

def get_script_path(script_name, experiment_base_dir):
    return os.path.join(experiment_base_dir, script_name)


def is_an_user_defined_module(imported_module, experiment_base_dir):
    return os.path.exists(get_script_path(imported_module, experiment_base_dir))


def module_script_already_analized(imported_module, scripts_analized):
    return imported_module in scripts_analized


def import_command_to_imported_modules(import_command, script_name):
    def module_name_to_module_path(module_name):
        module_path = module_name[0]
        for i in range(1, len(module_name), 1):
            letter = module_name[i]
            if((letter == "." and module_path[-1] != ".") or
            (letter != "." and module_path[-1] == ".")):
                module_path += os.sep + letter
            else:
                module_path += letter
        module_path += ".py" if module_path[-1] != "." else os.sep + "__init__.py"
        return os.path.normpath(os.path.join(os.path.dirname(script_name), module_path))

    imported_modules = []
    if(isinstance(import_command, ast.Import)):
        for alias in import_command.names:
            imported_modules.append(module_name_to_module_path(alias.name))

    elif(isinstance(import_command, ast.ImportFrom)):
        imported_module = import_command.level * "." + import_command.module if import_command.module is not None else import_command.level * "."
        imported_modules.append(module_name_to_module_path(imported_module))
        
    return imported_modules


def create_experiment_function_graph(user_script_path):
    experiment_base_dir, user_script_name = os.path.split(user_script_path)
    
    scripts_analized = {}
    scripts_to_be_analized = [user_script_name]
    while(len(scripts_to_be_analized) > 0):

        print("\n=============================================================================================================================================")
        print("scripts_analized:", scripts_analized)
        print("scripts_to_be_analized:", scripts_to_be_analized)
        print("script_path:", get_script_path(scripts_to_be_analized[0], experiment_base_dir))



        script_name = scripts_to_be_analized.pop(0)

        script_ast = python_code_to_AST(get_script_path(script_name, experiment_base_dir))
        if(script_ast is None):
            raise RuntimeError

        script_ASTSearcher = ASTSearcher(script_ast)
        script_ASTSearcher.search()
        
        for import_command in script_ASTSearcher.import_commands:
            imported_modules = import_command_to_imported_modules(import_command, script_name)


            print("")
            if isinstance(import_command, ast.Import):
                print("ast.Import")
                for alias in import_command.names:
                    print("    alias.name = {0}".format(alias.name))
                    print("    alias.asname = {0}\n".format(alias.asname))
            if isinstance(import_command, ast.ImportFrom):
                print("ast.ImportFrom")
                print("    module = {0}".format(import_command.module))
                print("    level = {0}".format(import_command.level))
                for alias in import_command.names:
                    print("    alias.name = {0}".format(alias.name))
                    print("    alias.asname = {0}\n".format(alias.asname))
            print("imported_modules:", imported_modules)
            

            
            for imported_module in imported_modules:

                print("")
                print("imported_module:", imported_module)
                print("is_an_user_defined_module:", is_an_user_defined_module(imported_module, experiment_base_dir))
                print("module_script_already_analized:", module_script_already_analized(imported_module, scripts_analized))
                print(get_script_path(imported_module, experiment_base_dir))



                if(imported_module.find("newintpy") != -1):
                    continue

                if(is_an_user_defined_module(imported_module, experiment_base_dir) and
                not module_script_already_analized(imported_module, scripts_analized)):
                    scripts_to_be_analized.append(imported_module)
        
        scripts_analized[script_name] = script_ASTSearcher
        """
        scripts_analized[script_name] = Script(script_ASTSearcher.AST,
                                        script_ASTSearcher.import_commands,
                                        script_ASTSearcher.functions)
        """    
    #################MODIFICAR O GRAFO
    experiment_scripts = []
    for script_name in scripts_analized:
        script_ASTSearcher = scripts_analized[script_name]
        if(script_name == user_script_path):
            script_name = "__main__"
        experiment_scripts.append(Script(script_name, script_ASTSearcher.AST, script_ASTSearcher.import_commands, script_ASTSearcher.functions))
    
    experimentFunctionGraphCreator = ExperimentFunctionGraphCreator(experiment_scripts)
    experimentFunctionGraphCreator.create_experiment_function_graph()
    return experimentFunctionGraphCreator.function_graph

    """
    #########DEBUG###########
    dictionary = function_class_method_searcher.functions
    #dictionary.update(function_class_method_searcher.instance_methods)
    #dictionary.update(function_class_method_searcher.class_methods)
    print("dictionary:", dictionary)
    USER_SCRIPT_GRAPH.print_graph(dictionary)

    print("")
    import ast
    for comandoImport in function_class_method_searcher.imported_modules:
        if isinstance(comandoImport, ast.Import):
            print("ast.Import")
            for alias in comandoImport.names:
                print("    alias.name = {0}".format(alias.name))
                print("    alias.asname = {0}\n".format(alias.asname))
        
        if isinstance(comandoImport, ast.ImportFrom):
            print("ast.ImportFrom")
            print("    module = {0}".format(comandoImport.module))
            print("    level = {0}".format(comandoImport.level))
            for alias in comandoImport.names:
                print("    alias.name = {0}".format(alias.name))
                print("    alias.asname = {0}\n".format(alias.asname))
        
    #########################
    """


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


class ASTSearcher(ast.NodeVisitor):
    def __init__(self, AST):
        self.__AST = AST
        self.__import_commands = []
        self.__functions = {}

    def search(self):
        #Finding all declared functions and imported modules
        #in the AST

        self.__current_function = None
        self.__current_function_name = ""
        self.visit(self.__AST)

    def visit_Import(self, node):
        if(node not in self.__import_commands):
            self.__import_commands.append(node)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if(node not in self.__import_commands):
            self.__import_commands.append(node)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """This function avoids that child nodes of a ClassDef node
        (ex.: class methods) be visited during search"""
        
    def visit_FunctionDef(self, node):
        previous_function_name = self.__current_function_name
        self.__current_function_name = node.name if self.__current_function_name == "" else self.__current_function_name + "." + node.name
        previous_function = self.__current_function
        self.__current_function = node


        self.__functions[self.__current_function_name] = node

        self.generic_visit(node)


        self.__current_function = previous_function
        self.__current_function_name = previous_function_name

    @property
    def AST(self):
        return self.__AST

    @property
    def import_commands(self):
        return self.__import_commands

    @property
    def functions(self):
        return self.__functions


class Script():
    def __init__(self, name, AST, import_commands, functions):
        self.__name = name
        self.__AST = AST
        self.__import_commands = import_commands
        self.__functions = functions

    @property
    def name(self):
        return self.__name

    @property
    def AST(self):
        return self.__AST

    @property
    def import_commands(self):
        return self.__import_commands

    @property
    def functions(self):
        return self.__functions


def get_script(experiment_scripts, script_name):
    for script in experiment_scripts:
        if(script.name == script_name):
            return script
    return None


class ExperimentFunctionGraphCreator(ast.NodeVisitor):
    def __init__(self, experiment_scripts):
        self.__experiment_scripts = experiment_scripts
        self.__experiment_function_graph = Graph()

    def create_experiment_function_graph(self):
        self.__create_script_function_graph("__main__")

    def __create_script_function_graph(self, script_name):
        script = get_script(self.__experiment_scripts, script_name)
        if(script is None):
            raise RuntimeError("Un unexpected error occurred while trying to create the experiment function graph!")

        function_graphs_of_imported_scripts = []
        for import_command in script.import_commands:
            imported_modules = import_command_to_imported_modules(import_command, script_name)
            
            for imported_module in imported_modules:
                script_graph = self.__create_script_function_graph(imported_module)
                









        for function in self.__functions.values():
            self.__function_graph.insert_vertice(GraphVertice(function))
        
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
