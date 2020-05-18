class InitCommandContext:
    """Init command context.

    :param connectivity: Connectivity details that can help connect to the APIs
    :type connectivity: ConnectivityContext

    :param resource: The details of the resource using the driver
    :type resource: ResourceContextDetails
    """

    def __init__(self, connectivity, resource):
        self.connectivity = connectivity
        self.resource = resource


class ResourceCommandContext:
    """Resource command context.

    :param connectivity: Connectivity details that can help connect to the APIs
    :type connectivity: ConnectivityContext

    :param resource: The details of the resource using the driver
    :type resource: ResourceContextDetails

    :param reservation: The details of the reservation
    :type reservation: ReservationContextDetails

    :param connectors: The list of visual connectors and routes that are connected
    to the resource (the resource will be considered as the source end point)
    :type connectors: list[Connector]
    """

    def __init__(self, connectivity, resource, reservation, connectors):
        self.connectivity = connectivity
        self.resource = resource
        self.reservation = reservation
        self.connectors = connectors


class ConnectivityContext:
    """Connectivity context.

    :param server_address: The address of the Quali server
    :type server_address: str

    :param cloudshell_api_port: the port of the TestShell API
    :type cloudshell_api_port: str

    :param quali_api_port: The port of the Quali API
    :type quali_api_port: str

    :param admin_auth_token: security token
    :type admin_auth_token: str

    :type cloudshell_version: str

    :type cloudshell_api_scheme: str
    """

    def __init__(
        self,
        server_address,
        cloudshell_api_port,
        quali_api_port,
        admin_auth_token,
        cloudshell_version,
        cloudshell_api_scheme,
    ):
        self.server_address = server_address
        self.cloudshell_api_port = cloudshell_api_port
        self.quali_api_port = quali_api_port
        self.admin_auth_token = admin_auth_token
        self.cloudshell_version = cloudshell_version
        self.cloudshell_api_scheme = cloudshell_api_scheme


class ResourceContextDetails:
    """Resource context details.

    :param id: The identifier of the resource / service / app - consistent value
    that can't be changed / renamed by the user
    :type id: str

    :param name: The name of the resource
    :type name: str

    :param fullname: The full name of the resource
    :type fullname: str

    :param type: The type of the resource  (Service, App, Resource)
    :type type: str

    :param address: The IP address of the resource
    :type address: str

    :param model: The resource model
    :type model: str

    :param family: The resource family
    :type family: str

    :param description: The resource description
    :type description: str

    :param attributes: A dictionary that contains the resource attributes
    (name, value)
    :type attributes: dict[str, str]

    :type app_context: AppContext

    :type shell_standard: str

    :type shell_standard_version: str
    """

    def __init__(
        self,
        id,  # noqa: A002
        name,
        fullname,
        type,  # noqa: A002
        address,
        model,
        family,
        description,
        attributes,
        app_context,
        networks_info,
        shell_standard,
        shell_standard_version,
    ):
        self.id = id
        self.name = name
        self.fullname = fullname
        self.type = type
        self.address = address
        self.model = model
        self.family = family
        self.description = description
        self.attributes = attributes
        self.app_context = app_context
        self.shell_standard = shell_standard
        self.shell_standard_version = shell_standard_version


class AppContext:
    """App context.

    :param app_request_json: app request details: selected deployment path
    :type app_request_json: str

    :param deployed_app_json: resource name, family, model, address, attributes
    names and values, vm details
    :type deployed_app_json: str
    """

    def __init__(self, app_request_json, deployed_app_json):
        self.app_request_json = app_request_json
        self.deployed_app_json = deployed_app_json


class InterfaceContextDetails:
    """Interface context details.

    :type type: str
    :type fullName: str
    """

    def __init__(self, interface):
        self.type = interface.Type
        self.fullName = interface.FullName


class Connector:
    """Connector.

    :param source: The name of the source resource (end point)
    :type source: str

    :param target: The name of the target resource (end point)
    :type target: str

    :param target_family: The family of the target resource
    :type target_family: str

    :param target_model: The model of the target resource
    :type target_model: str

    :param target_type: The type of the target resource  (Service, App, Resource)
    :type target_type: str

    :param target_attributes: A dictionary with the target resource
    attributes (name, value)
    :type target_attributes: dict[str, str]

    :param direction: The direction of the connection: Uni, Bi
    :type direction: str

    :param alias: The connection alias
    :type alias: str

    :param attributes: The dictionary that includes the connection
    attributes (name, value)
    :type attributes: dict[str, str]

    :param connection_type: The type of the connection: Route, Visual Connector,
    Physical
    :type connection_type: str
    """

    def __init__(
        self,
        source,
        target,
        target_family,
        target_model,
        target_type,
        target_attributes,
        direction,
        alias,
        attributes,
        connection_type,
    ):
        self.source = source
        self.target = target
        self.target_family = target_family
        self.target_model = target_model
        self.target_type = target_type
        self.target_attributes = target_attributes
        self.direction = direction
        self.alias = alias
        self.attributes = attributes
        self.connection_type = connection_type


class ReservationContextDetails:
    """Reservation context details.

    :param environment_name: The name of the environment
    :type environment_name: str

    :param environment_path: The full path of the environment
    :type environment_path: str

    :param domain: The reservation domain
    :type domain: str

    :param description: The reservation description
    :type description: str

    :param owner_user: the owner of the reservation
    :type owner_user: str

    :param owner_email: the email of the owner of the reservation
    :type owner_email: str

    :param reservation_id: The unique identifier of the reservation
    :type reservation_id: str

    :param saved_sandbox_name:
    :type saved_sandbox_name: str

    :param saved_sandbox_id:
    :type saved_sandbox_id: str

    :param running_user: The user that run the command
    :type running_user: str

    """

    def __init__(
        self,
        environment_name,
        environment_path,
        domain,
        description,
        owner_user,
        owner_email,
        reservation_id,
        saved_sandbox_name,
        saved_sandbox_id,
        running_user,
    ):
        self.reservation_id = reservation_id
        self.environment_name = environment_name
        self.environment_path = environment_path
        self.domain = domain
        self.description = description
        self.owner_user = owner_user
        self.owner_email = owner_email
        self.saved_sandbox_name = saved_sandbox_name
        self.saved_sandbox_id = saved_sandbox_id
        self.running_user = running_user


class CancellationContext:
    """Cancellation context.

    :type is_cancelled: bool
    """

    def __init__(self):
        self.is_cancelled = False


class AutoLoadCommandContext:
    """Autoload command context.

    :param connectivity: Connectivity details that can help connect to the APIs
    :type connectivity: ConnectivityContext

    :param resource: The details of the resource using the driver
    :type resource: ResourceContextDetails
    """

    def __init__(self, connectivity, resource):
        self.connectivity = connectivity
        self.resource = resource


class AutoLoadDetails:
    """AutoLoad details.

    :param resources: the list of resources (root and sub) that were discovered
    :type resources: list[AutoLoadResource]

    :param attributes: the list of attributes for the resources
    :type attributes: list[AutoLoadAttribute]
    """

    def __init__(self, resources, attributes):
        self.resources = resources
        self.attributes = attributes


class AutoLoadResource:
    """AutoLoad resource.

    :type model: str
    :type name: str
    :type relative_address: str
    :type unique_identifier: str
    """

    def __init__(self, model, name, relative_address, unique_identifier=None):
        self.model = model
        self.name = name
        self.relative_address = relative_address
        self.unique_identifier = unique_identifier


class AutoLoadAttribute:
    """AutoLoad attributes.

    :type relative_address: str
    :type attribute_name: str
    :type attribute_value: str
    """

    def __init__(self, relative_address, attribute_name, attribute_value):
        self.relative_address = relative_address
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value


class ResourceRemoteCommandContext:
    """Resource remote command context.

    :param connectivity: Connectivity details that can help connect to the APIs
    :type connectivity: ConnectivityContext

    :param resource: The details of the resource using the driver
    :type resource: ResourceContextDetails

    :param remote_reservation: The details of the remote reservation
    :type remote_reservation: ReservationContextDetails

    :type remote_endpoints: list[ResourceContextDetails]
    """

    def __init__(self, connectivity, resource, remote_reservation, remote_endpoints):
        self.connectivity = connectivity
        self.resource = resource
        self.remote_reservation = remote_reservation
        self.remote_endpoints = remote_endpoints


class ApiVmDetails(object):
    """API VM details.

    :param CloudProviderName: The name of the cloud provider
    :type CloudProviderName: str

    :param UID: UUID of the created VM
    :type UID: str

    :param VmCustomParams: VM custom parameters
    :type VmCustomParams: list[ApiVmCustomParam]
    """

    def __init__(self, cloud_provider_name="", uid="", vm_custom_params=None):
        self.CloudProviderName = cloud_provider_name
        self.UID = uid
        self.VmCustomParams = vm_custom_params or []


class ApiVmCustomParam(object):
    """API VM custom param.

    :type Name: str
    :type Value: str
    """

    def __init__(self, name="", value=""):
        self.Name = name
        self.Value = value
