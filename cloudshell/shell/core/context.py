class InitCommandContext:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.connectivity = None  # Connectivity details that can help connect to the APIs
        """:type : ConnectivityContext"""
        self.resource = None  # The details of the resource using the driver
        """:type : ResourceContextDetails"""


class ResourceCommandContext:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.connectivity = None  # Connectivity details that can help connect to the APIs
        """:type : ConnectivityContext"""
        self.resource = None  # The details of the resource using the driver
        """:type : ResourceContextDetails"""
        self.reservation = None  # The details of the reservation
        """:type : ReservationContextDetails"""
        self.connectors = None  # The list of visual connectors and routes that are connected to the resource (the resource will be considered as the source end point)
        """:type : list[Connector]"""


class ConnectivityContext:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.server_address = None  # The address of the Quali server
        """:type : str"""
        self.cloudshell_api_port = None  # the port of the TestShell API
        """:type : str"""
        self.quali_api_port = None  # The port of the Quali API
        """:type : str"""
        self.cloudshell_api_scheme = None  # The http scheme of the Quali API
        """:type : str"""
        self.admin_auth_token = None  # security token
        """:type : str"""


class ResourceContextDetails:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.id = None  # The identifier of the resource / service / app - consistent value that can't be changed / renamed by the user
        """:type : str"""
        self.name = None  # The name of the resource
        """:type : str"""
        self.fullname = None  # The full name of the resource
        """:type : str"""
        self.type = None  # The type of the resource  (Service, App, Resource)
        """:type : str"""
        self.address = None  # The IP address of the resource
        """:type : str"""
        self.model = None  # The resource model
        """:type : str"""
        self.family = None  # The resource family
        """:type : str"""
        self.description = None  # The resource description
        """:type : str"""
        self.attributes = None  # A dictionary that contains the resource attributes (name, value)
        """:type : dict[str,str]"""
        self.app_context = None
        """:type : AppContext"""


class AppContext:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.app_request_json = None  # app request details: selected deployment path
        """:type : str"""
        self.deployed_app_json = None  # resource name, family, model, address, attributes names and values, vm details
        """:type : str"""


class Connector:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.source = None  # The name of the source resource (end point)
        """:type : str"""
        self.target = None  # The name of the target resource (end point)
        """:type : str"""
        self.target_family = None  # The family of the target resource
        """:type : str"""
        self.target_model = None  # The model of the target resource
        """:type : str"""
        self.target_type = None  # The type of the target resource  (Service, App, Resource)
        """:type : str"""
        self.target_attributes = None  # A dictionary with the target resource attributes (name, value)
        """:type : dict[str,str]"""
        self.direction = None  # The direction of the connection: Uni, Bi
        """:type : str"""
        self.alias = None  # The connection alias
        """:type : str"""
        self.attributes = None  # The dictionary that includes the connection attributes (name, value)
        """:type : dict[str,str]"""
        self.connection_type = None  # The type of the connection: Route, Visual Connector, Physical
        """:type : str"""


class ReservationContextDetails:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.reservation_id = None  # The unique identifier of the reservation
        """:type : str"""
        self.environment_name = None  # The name of the environment
        """:type : str"""
        self.environment_path = None  # The full path of the environment
        """:type : str"""
        self.domain = None  # The reservation domain
        """:type : str"""
        self.description = None  # The reservation description
        """:type : str"""
        self.owner_user = None  # the owner of the reservation
        """:type : str"""
        self.owner_email = None  # the email of the owner of the reservation
        """:type : str"""


class CancellationContext:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.is_cancelled = None
        """:type : bool"""


class AutoLoadCommandContext:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.connectivity = None  # Connectivity details that can help connect to the APIs
        """:type : ConnectivityContext"""
        self.resource = None  # The details of the resource using the driver
        """:type : ResourceContextDetails"""


class AutoLoadDetails:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.resources = None    # the list of resources (root and sub) that were discovered
        """:type : list[AutoLoadResource]"""
        self.attributes = None  # the list of attributes for the resources
        """:type : list[AutoLoadAttribute]"""


class AutoLoadResource:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.model = None
        """:type : str"""
        self.name = None
        """:type : str"""
        self.relative_address = None
        """:type : str"""
        self.unique_identifier = None
        """:type : str"""


class AutoLoadAttribute:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.relative_address = None
        """:type : str"""
        self.attribute_name = None
        """:type : str"""
        self.attribute_value = None
        """:type : str"""


class ResourceRemoteCommandContext:
    ATTRIBUTE_MAP = {}

    def __init__(self):
        self.connectivity = None  # Connectivity details that can help connect to the APIs
        """:type : ConnectivityContext"""
        self.resource = None  # The details of the resource using the driver
        """:type : ResourceContextDetails"""
        self.remote_reservation = None  # The details of the remote reservation
        """:type : ReservationContextDetails"""
        self.remote_endpoints = None
        """:type : list[ResourceContextDetails]"""
