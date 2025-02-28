.. _api-network:

===========
Network API
===========

The ``network`` package holds classes for interacting with the Ethereum blockchain. This is the most extensive package within Brownie and contains the majority of the user-facing functionality.

``brownie.network.main``
========================

The ``main`` module contains methods for conncting to or disconnecting from the network. All of these methods are available directly from ``brownie.network``.

.. py:method:: main.connect(network: str = None, launch_rpc: bool = True) -> None

    Connects to the network.  Network settings are retrieved from ``brownie-config.yaml``

    * ``network``: The network to connect to. If ``None``, connects to the default network as specified in the config file.
    * ``launch_rpc``: If ``True`` and the configuration for this network includes ``test_rpc`` settings, attempts to launch or attach to a local RPC client. See :ref:`test-rpc` for detailed information on the sequence of events in this process.

    Calling this method is favored over calling ``web3.connect`` and ``rpc.launch`` or ``rpc.attach`` individually.

    .. code-block:: python

        >>> from brownie import network
        >>> network.connect('development')

.. py:method:: main.disconnect(kill_rpc: bool = True) -> None

    Disconnects from the network.

    The ``Web3`` provider is cleared, the active network is set to ``None`` and the local RPC client is terminated if it was launched as a child process.

    .. code-block:: python

        >>> from brownie import network
        >>> network.disconnect()

.. py:method:: main.is_connected() -> bool

    Returns ``True`` if the ``Web3`` object is connected to the network.

    .. code-block:: python

        >>> from brownie import network
        >>> network.is_connected()
        True

.. py:method:: main.show_active() -> Optional[str]

    Returns the name of the network that is currently active, or ``None`` if not connected.

    .. code-block:: python

        >>> from brownie import network
        >>> network.show_active()
        'development'

.. py:method:: main.gas_limit(*args: Tuple[Union[int, str, bool, None]]) -> Union[int, bool]

    Gets and optionally sets the default gas limit.

    * If no argument is given, the current default is displayed.
    * If an integer value is given, this will be the default gas limit.
    * If set to ``None``, ``True`` or ``False``, the gas limit is determined automatically via ``web3.eth.estimateGas``.

    Returns ``False`` if the gas limit is set automatically, or an ``int`` if it is set to a fixed value.

    .. code-block:: python

        >>> from brownie import network
        >>> network.gas_limit()
        False
        >>> network.gas_limit(6700000)
        6700000
        >>> network.gas_limit(None)
        False

.. py:method:: main.gas_price(*args: Tuple[Union[int, str, bool, None]]) -> Union[int, bool]

    Gets and optionally sets the default gas price.

    * If an integer value is given, this will be the default gas price.
    * If set to ``None``, ``True`` or ``False``, the gas price is determined automatically via ``web3.eth.getPrice``.

    Returns ``False`` if the gas price is set automatically, or an ``int`` if it is set to a fixed value.

    .. code-block:: python

        >>> from brownie import network
        >>> network.gas_price()
        False
        >>> network.gas_price(10000000000)
        10000000000
        >>> network.gas_price("1.2 gwei")
        1200000000
        >>> network.gas_price(False)
        False

``brownie.network.account``
===========================

The ``account`` module holds classes for interacting with Ethereum accounts for which you control the private key.

Classes in this module are not meant to be instantiated directly. The ``Accounts`` container is available as ``accounts`` (or just ``a``) and will create each ``Account`` automatically during initialization. Add more accounts using ``Accounts.add``.

.. _api-network-accounts:

Accounts
--------

.. py:class:: brownie.network.account.Accounts

    List-like :ref:`Singleton<api-types-singleton>` container that holds all of the available accounts as ``Account`` or ``LocalAccount`` objects. When printed it will display as a list.

    .. code-block:: python

        >>> from brownie.network import accounts
        >>> accounts
        [<Account object '0x7Ebaa12c5d1EE7fD498b51d4F9278DC45f8D627A'>, <Account object '0x186f79d227f5D819ACAB0C529031036D11E0a000'>, <Account object '0xC53c27492193518FE9eBff00fd3CBEB6c434Cf8b'>, <Account object '0x2929AF7BBCde235035ED72029c81b71935c49e94'>, <Account object '0xb93538FEb07b3B8433BD394594cA3744f7ee2dF1'>, <Account object '0x1E563DBB05A10367c51A751DF61167dE99A4d0A7'>, <Account object '0xa0942deAc0885096D8400D3369dc4a2dde12875b'>, <Account object '0xf427a9eC1d510D77f4cEe4CF352545071387B2e6'>, <Account object '0x2308D528e4930EFB4aF30793A3F17295a0EFa886'>, <Account object '0x2fb37EB570B1eE8Eda736c1BD1E82748Ec3d0Bf1'>]
        >>> dir(accounts)
        [add, at, clear, load, remove]

Accounts Methods
****************

.. py:classmethod:: Accounts.add(priv_key=None)

    Creates a new ``LocalAccount`` with private key ``priv_key``, appends it to the container, and returns the new account instance.  If no private key is entered, one is randomly generated via ``os.urandom(8192)``.

    .. code-block:: python

        >>> accounts.add()
        <Account object '0xb094716BC0E9D3F3Fb42FF928bd76618435FeeAA'>
        >>> accounts.add('8fa2fdfb89003176a16b707fc860d0881da0d1d8248af210df12d37860996fb2')
        <Account object '0xc1826925377b4103cC92DeeCDF6F96A03142F37a'>

.. py:classmethod:: Accounts.at(address)

    Given an address as a string, returns the corresponding ``Account`` or ``LocalAccount`` from the container.

    .. code-block:: python

        >>> accounts.at('0xc1826925377b4103cC92DeeCDF6F96A03142F37a')
        <Account object '0xc1826925377b4103cC92DeeCDF6F96A03142F37a'>

.. py:classmethod:: Accounts.clear()

    Empties the container.

    .. code-block:: python

        >>> accounts.clear()

.. py:classmethod:: Accounts.load(filename=None)

    Decrypts a `keystore <https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition>`__ file and returns a ``LocalAccount`` object.

    Brownie will first attempt to find the keystore file as a path relative to the loaded project. If not found, it will look in the ``brownie/data/accounts`` folder within the Brownie package.

    If filename is ``None``, returns a list of available keystores in ``brownie/data/accounts``.

    .. code-block:: python

        >>> accounts.load()
        ['my_account']
        >>> accounts.load('my_account')
        Enter the password for this account:
        <LocalAccount object '0xa9c2DD830DfFE8934fEb0A93BAbcb6e823e1FF05'>

.. py:classmethod:: Accounts.remove(address)

    Removes an address from the container. The address may be given as a string or an ``Account`` instance.

    .. code-block:: python

        >>> accounts.remove('0xc1826925377b4103cC92DeeCDF6F96A03142F37a')

Accounts Internal Methods
*************************

.. py:classmethod:: Accounts._reset()

    Called by :ref:`rpc._notify_registry <api-network-rpc-notify-registry>` when the local chain has been reset. All ``Account`` objects are recreated.

.. py:classmethod:: Accounts._revert(height)

    Called by :ref:`rpc._notify_registry <api-network-rpc-notify-registry>` when the local chain has been reverted to a block height greater than zero. Adjusts ``Account`` object nonce values.

.. _api-network-account:

Account
-------

.. py:class:: brownie.network.account.Account

    An ethereum address that you control the private key for, and so can send transactions from. Generated automatically from ``web3.eth.accounts`` and stored in the ``Accounts`` container.

    .. code-block:: python

        >>> accounts[0]
        <Account object '0x7Ebaa12c5d1EE7fD498b51d4F9278DC45f8D627A'>
        >>> dir(accounts[0])
        [address, balance, deploy, estimate_gas, nonce, transfer]

Account Attributes
******************

.. py:attribute:: Account.address

    The public address of the account. Viewable by printing the class, you do not need to call this attribute directly.

    .. code-block:: python

        >>> accounts[0].address
        '0x7Ebaa12c5d1EE7fD498b51d4F9278DC45f8D627A'

.. py:attribute:: Account.nonce

    The current nonce of the address.

    .. code-block:: python

        >>> accounts[0].nonce
        0

Account Methods
***************

.. py:classmethod:: Account.balance()

    Returns the current balance at the address, in :ref:`wei<wei>`.

    .. code-block:: python

        >>> accounts[0].balance()
        100000000000000000000
        >>> accounts[0].balance() == "100 ether"
        True

.. py:classmethod:: Account.deploy(contract, *args, amount=None, gas_limit=None, gas_price=None)

    Deploys a contract.

    * ``contract``: A ``ContractContainer`` instance of the contract to be deployed.
    * ``*args``: Contract constructor arguments.
    * ``amount``: Amount of ether to send with the transaction. The given value is converted to :ref:`wei <wei>`.
    * ``gas_limit``: Gas limit for the transaction. The given value is converted to :ref:`wei <wei>`. If none is given, the price is set using ``eth_estimateGas``.
    * ``gas_price``: Gas price for the transaction. The given value is converted to :ref:`wei <wei>`. If none is given, the price is set using ``eth_gasPrice``.

    Returns a ``Contract`` instance upon success. If the transaction reverts or you do not wait for a confirmation, a ``TransactionReceipt`` is returned instead.

    .. code-block:: python

        >>> Token
        []
        >>> t = accounts[0].deploy(Token, "Test Token", "TST", 18, "1000 ether")

        Transaction sent: 0x2e3cab83342edda14141714ced002e1326ecd8cded4cd0cf14b2f037b690b976
        Transaction confirmed - block: 1   gas spent: 594186
        Contract deployed at: 0x5419710735c2D6c3e4db8F30EF2d361F70a4b380
        <Token Contract object '0x5419710735c2D6c3e4db8F30EF2d361F70a4b380'>
        >>>
        >>> t
        <Token Contract object '0x5419710735c2D6c3e4db8F30EF2d361F70a4b380'>
        >>> Token
        [<Token Contract object '0x5419710735c2D6c3e4db8F30EF2d361F70a4b380'>]
        >>> Token[0]
        <Token Contract object '0x5419710735c2D6c3e4db8F30EF2d361F70a4b380'>

.. py:classmethod:: Account.estimate_gas(to, amount, data="")

    Estimates the gas required to perform a transaction. Raises a ``VirtualMachineError`` if the transaction would revert.

    The returned value is given as an ``int`` denominated in wei.

    * ``to``: Recipient address. Can be an ``Account`` instance or string.
    * ``amount``: Amount of ether to send. The given value is converted to :ref:`wei <wei>`.
    * ``data``: Transaction data hexstring.

    .. code-block:: python

        >>> accounts[0].estimate_gas(accounts[1], "1 ether")
        21000

.. py:classmethod:: Account.transfer(self, to, amount, gas_limit=None, gas_price=None, data="")

    Broadcasts a transaction from this account.

    * ``to``: Recipient address. Can be an ``Account`` instance or string.
    * ``amount``: Amount of ether to send. The given value is converted to :ref:`wei <wei>`.
    * ``gas_limit``: Gas limit for the transaction. The given value is converted to :ref:`wei <wei>`. If none is given, the price is set using ``eth_estimateGas``.
    * ``gas_price``: Gas price for the transaction. The given value is converted to :ref:`wei <wei>`. If none is given, the price is set using ``eth_gasPrice``.
    * ``data``: Transaction data hexstring.

    Returns a ``TransactionReceipt`` instance.

    .. code-block:: python

        >>> accounts[0].transfer(accounts[1], "1 ether")

        Transaction sent: 0x0173aa6938c3a5e50b6dc7b4d38e16dab40811ab4e00e55f3e0d8be8491c7852
        Transaction confirmed - block: 1   gas used: 21000 (100.00%)
        <Transaction object '0x0173aa6938c3a5e50b6dc7b4d38e16dab40811ab4e00e55f3e0d8be8491c7852'>

LocalAccount
------------

.. py:class:: brownie.network.account.LocalAccount

    Functionally identical to ``Account``. The only difference is that a ``LocalAccount`` is one where the private key was directly inputted, and so is not found in ``web3.eth.accounts``.

    .. note:: Resetting the RPC client will delete all ``LocalAccount`` objects from the ``Accounts`` container.

    .. code-block:: python

        >>> accounts.add()
        <LocalAccount object '0x716E8419F2926d6AcE07442675F476ace972C580'>
        >>> accounts[-1]
        <LocalAccount object '0x716E8419F2926d6AcE07442675F476ace972C580'>

LocalAccount Attributes
***********************

.. py:attribute:: LocalAccount.public_key

    The local account's public key as a string.

    .. code-block:: python

        >>> accounts[-1].public_key
        '0x34b51e2913f5771acdddea7d353404f844b02a39ad4003c08afaa729993c43e890181327beaf352d81424cd277f4badc55be789a2817ea097bc82ea4801fee5b'

.. py:attribute:: LocalAccount.private_key

    The local account's private key as a string.

    .. code-block:: python

        >>> accounts[-1].private_key
        '0xd289bec8d9ad145aead13911b5bbf01936cbcd0efa0e26d5524b5ad54a61aeb8'

LocalAccount Methods
********************

.. py:classmethod:: LocalAccount.save(filename, overwrite=False)

    Saves the account's private key in an encrypto `keystore <https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition>`__ file.

    If the filename does not include a folder, the keystore is saved in the ``brownie/data/accounts`` folder within the Brownie package.

    Returns the absolute path to the keystore file, as a string.

    .. code-block:: python

        >>> accounts[-1].save('my_account')
        Enter the password to encrypt this account with:
        /python3.6/site-packages/brownie/data/accounts/my_account.json
        >>>
        >>> accounts[-1].save('~/my_account.json')
        Enter the password to encrypt this account with:
        /home/computer/my_account.json

PublicKeyAccount
----------------

.. py:class:: brownie.network.account.PublicKeyAccount

    Object for interacting with an Ethereum account where you do not control the private key. Can be used to check balances or to send ether to that address.

    .. code-block:: python

        >>> from brownie.network.account import PublicKeyAccount
        >>> pub = PublicKeyAccount("0x14b0Ed2a7C4cC60DD8F676AE44D0831d3c9b2a9E")
        <PublicKeyAccount object '0x14b0Ed2a7C4cC60DD8F676AE44D0831d3c9b2a9E'>

    Along with regular addresses, ``PublicKeyAccount`` objects can be instantiated using `ENS domain names <https://ens.domains/>`_. The returned object will have the resolved address.

    .. code-block:: python

        >>> PublicKeyAccount("ens.snakecharmers.eth")
        <PublicKeyAccount object '0x808B53bF4D70A24bA5cb720D37A4835621A9df00'>

.. py:classmethod:: PublicKeyAccount.balance()

    Returns the current balance at the address, in :ref:`wei<wei>`.

    .. code-block:: python

        >>> pub.balance()
        1000000000000000000

.. py:attribute:: PublicKeyAccount.nonce

    The current nonce of the address.

    .. code-block:: python

        >>> accounts[0].nonce
        0

``brownie.network.alert``
=========================

The ``alert`` module is used to set up notifications and callbacks based on state changes in the blockchain.

Alert
-----

Alerts and callbacks are handled by creating instances of the ``Alert`` class.

.. py:class:: brownie.network.alert.Alert(fn, args=None, kwargs=None, delay=2, msg=None, callback=None, repeat=False)

    An alert object. It is active immediately upon creation of the instance.

    * ``fn``: A callable to check for the state change.
    * ``args``: Arguments to supply to the callable.
    * ``kwargs``: Keyword arguments to supply to the callable.
    * ``delay``: Number of seconds to wait between checking for changes.
    * ``msg``: String to display upon change. The string will have ``.format(initial_value, new_value)`` applied before displaying.
    * ``callback``: A callback function to call upon a change in value. It should accept two arguments, the initial value and the new value.
    * ``repeat``: If ``False``, the alert will terminate after the first time it first. if ``True``, it will continue to fire with each change until it is stopped via ``Alert.stop()``.  If an ``int`` value is given, it will fire a total of ``n+1`` times before terminating.

    Alerts are **non-blocking**, threading is used to monitor changes. Once an alert has finished running it cannot be restarted.

    A basic example of an alert, watching for a changed balance:

    .. code-block:: python

        >>> from brownie.network.alert import Alert
        >>> Alert(accounts[1].balance, msg="Account 1 balance has changed from {} to {}")
        <brownie.network.alert.Alert object at 0x7f9fd25d55f8>

        >>> alert.show()
        [<brownie.network.alert.Alert object at 0x7f9fd25d55f8>]
        >>> accounts[2].transfer(accounts[1], "1 ether")

        Transaction sent: 0x912d6ac704e7aaac01be159a4a36bbea0dc0646edb205af95b6a7d20945a2fd2
        Transaction confirmed - block: 1   gas spent: 21000
        <Transaction object '0x912d6ac704e7aaac01be159a4a36bbea0dc0646edb205af95b6a7d20945a2fd2'>
        ALERT: Account 1 balance has changed from 100000000000000000000 to 101000000000000000000

    This example uses the alert's callback function to perform a token transfer, and sets a second alert to watch for the transfer:

    .. code-block:: python

        >>> alert.new(accounts[3].balance, msg="Account 3 balance has changed from {} to {}")
        <brownie.network.alert.Alert object at 0x7fc743e415f8>

        >>> def on_receive(old_value, new_value):
        ...     accounts[2].transfer(accounts[3], new_value-old_value)

        >>> alert.new(accounts[2].balance, callback=on_receive)
        <brownie.network.alert.Alert object at 0x7fc743e55cf8>
        >>> accounts[1].transfer(accounts[2],"1 ether")

        Transaction sent: 0xbd1bade3862f181359f32dac02ffd1d145fdfefc99103ca0e3d28ffc7071a9eb
        Transaction confirmed - block: 1   gas spent: 21000
        <Transaction object '0xbd1bade3862f181359f32dac02ffd1d145fdfefc99103ca0e3d28ffc7071a9eb'>

        Transaction sent: 0x8fcd15e38eed0a5c9d3d807d593b0ea508ba5abc892428eb2e0bb0b8f7dc3083
        Transaction confirmed - block: 2   gas spent: 21000
        ALERT: Account 3 balance has changed from 100000000000000000000 to 101000000000000000000

.. py:classmethod:: Alert.is_alive()

    Returns a boolean indicating if an alert is currently running.

    .. code-block:: python

        >>> a.is_alive()
        True

.. py:classmethod:: Alert.wait(timeout=None)

    Blocks until an alert has completed firing or the timeout value is reached. Similar to ``Thread.join()``.

    .. code-block:: python

        >>> a.wait()

.. py:classmethod:: Alert.stop(wait=True)

    Stops the alert.

    .. code-block:: python

        >>> alert_list = alert.show()
        [<brownie.network.alert.Alert object at 0x7f9fd25d55f8>]
        >>> alert_list[0].stop()
        >>> alert.show()
        []

Module Methods
--------------

.. py:method:: alert.new(fn, args=[], kwargs={}, delay=0.5, msg=None, callback=None, repeat=False)

    Alias for creating a new ``Alert`` instance.

    .. code-block:: python

        >>> from brownie import alert
        >>> alert.new(accounts[3].balance, msg="Account 3 balance has changed from {} to {}")
        <brownie.network.alert.Alert object at 0x7fc743e415f8>

.. py:method:: alert.show()

    Returns a list of all currently active alerts.

    .. code-block:: python

        >>> alert.show()
        [<brownie.network.alert.Alert object at 0x7f9fd25d55f8>]

.. py:method:: alert.stop_all()

    Stops all currently active alerts.

    .. code-block:: python

        >>> alert.show()
        [<brownie.network.alert.Alert object at 0x7f9fd25d55f8>]
        >>> alert.stop_all()
        >>> alert.show()
        []

``brownie.network.contract``
============================

The ``contract`` module contains classes for deploying and interacting with smart contracts.

When a project is loaded, Brownie automatically creates ``ContractContainer`` instances from on the files in the ``contracts/`` folder. New ``ProjectContract`` instances are created via methods in the container.

If you wish to interact with a contract outside of a project where only the ABI is available, use the ``Contract`` class.

Arguments supplied to calls or transaction methods are converted using the methods outlined in the :ref:`convert<api-brownie-convert>` module.

.. _api-network-contractcontainer:

ContractContainer
-----------------

.. py:class:: brownie.network.contract.ContractContainer

    A list-like container class that holds all ``ProjectContract`` instances of the same type, and is used to deploy new instances of that contract.

    .. code-block:: python

        >>> Token
        []
        >>> dir(Token)
        [abi, at, bytecode, deploy, remove, signatures, topics, tx]

ContractContainer Attributes
****************************

.. py:attribute:: ContractContainer.abi

    The ABI of the contract.

    >>> Token.abi
    [{'constant': True, 'inputs': [], 'name': 'name', 'outputs': [{'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'name': '_spender', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}], 'name': 'approve', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, ... ]

.. py:attribute:: ContractContainer.bytecode

    The bytecode of the contract, without any applied constructor arguments.

    >>> Token.bytecode
    '608060405234801561001057600080fd5b506040516107873803806107878339810160409081528151602080840151928401516060850151928501805190959490940193909291610055916000918701906100d0565b5082516100699060019060208601906100d0565b50600282905560038190553360008181526004602090815 ...

.. py:attribute:: ContractContainer.signatures

    A dictionary of bytes4 signatures for each contract method.

    If you have a signature and need to find the method name, use ``ContractContainer.get_method``.

    .. code-block:: python

        >>> Token.signatures
        {
            'allowance': "0xdd62ed3e",
            'approve': "0x095ea7b3",
            'balanceOf': "0x70a08231",
            'decimals': "0x313ce567",
            'name': "0x06fdde03",
            'symbol': "0x95d89b41",
            'totalSupply': "0x18160ddd",
            'transfer': "0xa9059cbb",
            'transferFrom': "0x23b872dd"
        }
        >>> Token.signatures.keys()
        dict_keys(['name', 'approve', 'totalSupply', 'transferFrom', 'decimals', 'balanceOf', 'symbol', 'transfer', 'allowance'])
        >>> Token.signatures['transfer']
        0xa9059cbb

.. py:attribute:: ContractContainer.topics

    A dictionary of bytes32 topics for each contract event.

    .. code-block:: python

        >>> Token.topics
        {
            'Approval': "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
            'Transfer': "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
        }
        >>> Token.topics.keys()
        dict_keys(['Transfer', 'Approval'])
        >>> Token.topics['Transfer']
        0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef

ContractContainer Methods
*************************

.. py:classmethod:: ContractContainer.deploy(*args)

    Deploys the contract.

    * ``*args``: Contract constructor arguments.

    You can optionally include a dictionary of `transaction parameters <https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.sendTransaction>`__ as the final argument. If you omit this or do not specify a ``'from'`` value, the transaction will be sent from the same address that deployed the contract.

    If the contract requires a library, the most recently deployed one will be used. If the required library has not been deployed yet an ``IndexError`` is raised.

    Returns a ``ProjectContract`` object upon success.

    In the console if the transaction reverts or you do not wait for a confirmation, a ``TransactionReceipt`` is returned instead.

    .. code-block:: python

        >>> Token
        []
        >>> Token.deploy
        <ContractConstructor object 'Token.constructor(string,string,uint256,uint256)'>
        >>> t = Token.deploy("Test Token", "TST", 18, "1000 ether", {'from': accounts[1]})

        Transaction sent: 0x2e3cab83342edda14141714ced002e1326ecd8cded4cd0cf14b2f037b690b976
        Transaction confirmed - block: 1   gas spent: 594186
        Contract deployed at: 0x5419710735c2D6c3e4db8F30EF2d361F70a4b380
        <Token Contract object '0x5419710735c2D6c3e4db8F30EF2d361F70a4b380'>
        >>>
        >>> t
        <Token Contract object '0x5419710735c2D6c3e4db8F30EF2d361F70a4b380'>
        >>> Token
        [<Token Contract object '0x5419710735c2D6c3e4db8F30EF2d361F70a4b380'>]
        >>> Token[0]
        <Token Contract object '0x5419710735c2D6c3e4db8F30EF2d361F70a4b380'>

.. py:classmethod:: ContractContainer.at(address, owner=None)

    Returns a ``ProjectContract`` instance.

    * ``address``: Address where the contract is deployed. Raises a ValueError if there is no bytecode at the address.
    * ``owner``: ``Account`` instance to set as the contract owner. If transactions to the contract do not specify a ``'from'`` value, they will be sent from this account.

    .. code-block:: python

        >>> Token
        [<Token Contract object '0x79447c97b6543F6eFBC91613C655977806CB18b0'>]
        >>> Token.at('0x79447c97b6543F6eFBC91613C655977806CB18b0')
        <Token Contract object '0x79447c97b6543F6eFBC91613C655977806CB18b0'>
        >>> Token.at('0xefb1336a2E6B5dfD83D4f3a8F3D2f85b7bfb61DC')
        File "brownie/lib/console.py", line 82, in _run
            exec('_result = ' + cmd, self.__dict__, local_)
        File "<string>", line 1, in <module>
        File "brownie/lib/components/contract.py", line 121, in at
            raise ValueError("No contract deployed at {}".format(address))
        ValueError: No contract deployed at 0xefb1336a2E6B5dfD83D4f3a8F3D2f85b7bfb61DC


.. py:classmethod:: ContractContainer.get_method(calldata)

    Given the call data of a transaction, returns the name of the contract method as a string.

    .. code-block:: python

        >>> tx = Token[0].transfer(accounts[1], 1000)

        Transaction sent: 0xc1fe0c7c8fd08736718aa9106662a635102604ea6db4b63a319e43474de0b420
        Token.transfer confirmed - block: 3   gas used: 35985 (26.46%)
        <Transaction object '0xc1fe0c7c8fd08736718aa9106662a635102604ea6db4b63a319e43474de0b420'>
        >>> tx.input
        0xa9059cbb00000000000000000000000066ace0365c25329a407002d22908e25adeacb9bb00000000000000000000000000000000000000000000000000000000000003e8
        >>> Token.get_method(tx.input)
        transfer

.. py:classmethod:: ContractContainer.remove(address)

    Removes a contract instance from the container.

    .. code-block:: python

        >>> Token
        [<Token Contract object '0x79447c97b6543F6eFBC91613C655977806CB18b0'>]
        >>> Token.remove('0x79447c97b6543F6eFBC91613C655977806CB18b0')
        >>> Token
        []

ContractContainer Internal Methods
**********************************

.. py:classmethod:: ContractContainer._reset()

    Called by :ref:`rpc._notify_registry <api-network-rpc-notify-registry>` when the local chain has been reset. All ``Contract`` objects are removed from the container and marked as :ref:`reverted <api-contract-reverted>`.

.. py:classmethod:: ContractContainer._revert(height)

    Called by :ref:`rpc._notify_registry <api-network-rpc-notify-registry>` when the local chain has been reverted to a block height greater than zero. Any ``Contract`` objects that no longer exist are removed from the container and marked as :ref:`reverted <api-contract-reverted>`.

.. _api-network-contract:

Contract and ProjectContract
----------------------------

``Contract`` and ``ProjectContract`` are both used to call or send transactions to smart contracts.

* ``Contract`` objects are instantiated directly and only require an ABI. They are used for calls to existing contracts that exist outside of a project.
* ``ProjectContract`` objects are created by calls to ``ContractContainer.deploy``. Because they are compiled and deployed directly by Brownie, they provide much greater debugging capability.

These classes have identical APIs.

.. py:class:: brownie.network.contract.Contract(name, address=None, abi=None, manifest_uri=None, owner=None)

    A deployed contract. This class allows you to call or send transactions to the contract.

    * ``name``: The name of the contract.
    * ``address``: Address of the contract. Required unless a ``manifest_uri`` is given.
    * ``abi``: ABI of the contract. Required unless a ``manifest_uri`` is given.
    * ``manifest_uri``: EthPM registry manifest uri. If given, the ABI (and optionally the contract address) are retrieved from here.
    * ``owner``: An optional ``Account`` instance. If given, transactions to the contract are sent broadcasted from this account by default.

    .. code-block:: python

        >>> from brownie import Contract
        >>> Contract('0x79447c97b6543F6eFBC91613C655977806CB18b0', "Token", abi)
        <Token Contract object '0x79447c97b6543F6eFBC91613C655977806CB18b0'>

.. py:class:: brownie.network.contract.ProjectContract

    A deployed contract that is part of an active Brownie project. Along with making calls and transactions, this object allows access to Brownie's full range of debugging and testing capability.

    .. code-block:: python

        >>> Token[0]
        <Token Contract object '0x79447c97b6543F6eFBC91613C655977806CB18b0'>
        >>> dir(Token[0])
        [abi, allowance, approve, balance, balanceOf, bytecode, decimals, name, signatures, symbol, topics, totalSupply, transfer, transferFrom, tx]

Contract Attributes
*******************

.. py:attribute:: Contract.bytecode

    The bytecode of the deployed contract, including constructor arguments.

    .. code-block:: python

        >>> Token[0].bytecode
        '6080604052600436106100985763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166306fdde03811461009d578063095ea7b31461012757806318160ddd1461015f57806323b872dd14610186578063313ce567146101b057806370a08231146101c557806395d89b41...

.. py:attribute:: Contract.tx

    The ``TransactionReceipt`` of the transaction that deployed the contract. If the contract was not deployed during this instance of brownie, it will be ``None``.

    .. code-block:: python

        >>> Token[0].tx
        <Transaction object '0xcede03c7e06d2b4878438b08cd0cf4515942b3ba06b3cfd7019681d18bb8902c'>

Contract Methods
****************

.. py:classmethod:: Contract.balance()

    Returns the current balance at the contract address, in :ref:`wei<wei>`.

    .. code-block:: python

        >>> Token[0].balance
        0

Contract Internal Attributes
****************************

.. _api-contract-reverted:

.. py:attribute:: Contract._reverted

    Boolean. Once set to to ``True``, any attempt to interact with the object raises a ``ContractNotFound`` exception. Set as a result of a call to :ref:`rpc._notify_registry <api-network-rpc-notify-registry>`.

.. _api-contract-call:

ContractCall
------------

.. py:class:: brownie.network.contract.ContractCall(*args)

    Calls a non state-changing contract method without broadcasting a transaction, and returns the result. ``args`` must match the required inputs for the method.

    The expected inputs are shown in the method's ``__repr__`` value.

    Inputs and return values are formatted via methods in the :ref:`convert<api-brownie-convert>` module. Multiple values are returned inside a :ref:`ReturnValue<return_value>`.

    .. code-block:: python

        >>> Token[0].allowance
        <ContractCall object 'allowance(address,address)'>
        >>> Token[0].allowance(accounts[0], accounts[2])
        0

ContractCall Attributes
***********************

.. py:attribute:: ContractCall.abi

    The contract ABI specific to this method.

    .. code-block:: python

        >>> Token[0].allowance.abi
        {
            'constant': True,
            'inputs': [{'name': '_owner', 'type': 'address'}, {'name': '_spender', 'type': 'address'}],
            'name': "allowance",
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': "view",
            'type': "function"
        }

.. py:attribute:: ContractCall.signature

    The bytes4 signature of this method.

    .. code-block:: python

        >>> Token[0].allowance.signature
        '0xdd62ed3e'

ContractCall Methods
********************

.. py:classmethod:: ContractCall.transact(*args)

    Sends a transaction to the method and returns a ``TransactionReceipt``.

    .. code-block:: python

        >>> tx = Token[0].allowance.transact(accounts[0], accounts[2])

        Transaction sent: 0xc4f3a0addfe1e475c2466f30c750ca7a60450132b07102af610d8d56f170046b
        Token.allowance confirmed - block: 2   gas used: 24972 (19.98%)
        <Transaction object '0xc4f3a0addfe1e475c2466f30c750ca7a60450132b07102af610d8d56f170046b'>
        >>> tx.return_value
        0

.. _api-contract-tx:

ContractTx
----------

.. py:class:: brownie.network.contract.ContractTx(*args)

    Broadcasts a transaction to a potentially state-changing contract method. Returns a ``TransactionReceipt``.

    The given ``args`` must match the required inputs for the method. The expected inputs are shown in the method's ``__repr__`` value.

    Inputs are formatted via methods in the :ref:`convert<api-brownie-convert>` module.

    You can optionally include a dictionary of `transaction parameters <https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.sendTransaction>`__ as the final argument. If you omit this or do not specify a ``'from'`` value, the transaction will be sent from the same address that deployed the contract.

    .. code-block:: python

        >>> Token[0].transfer
        <ContractTx object 'transfer(address,uint256)'>
        >>> Token[0].transfer(accounts[1], 100000, {'from':accounts[0]})

        Transaction sent: 0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0
        Transaction confirmed - block: 2   gas spent: 51049
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>

ContractTx Attributes
*********************

.. py:attribute:: ContractTx.abi

    The contract ABI specific to this method.

    .. code-block:: python

        >>> Token[0].transfer.abi
        {
            'constant': False,
            'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
            'name': "transfer",
            'outputs': [{'name': '', 'type': 'bool'}],
            'payable': False,
            'stateMutability': "nonpayable",
            'type': "function"
        }

.. py:attribute:: ContractTx.signature

    The bytes4 signature of this method.

    .. code-block:: python

        >>> Token[0].transfer.signature
        '0xa9059cbb'

ContractTx Methods
******************

.. py:classmethod:: ContractTx.call(*args)

    Calls the contract method without broadcasting a transaction, and returns the result.

    Inputs and return values are formatted via methods in the :ref:`convert<api-brownie-convert>` module. Multiple values are returned inside a :ref:`ReturnValue<return_value>`.

    .. code-block:: python

        >>> Token[0].transfer.call(accounts[2], 10000, {'from': accounts[0]})
        True

.. py:classmethod:: ContractTx.encode_input(*args)

    Returns a hexstring of ABI calldata that can be used to call the method with the given arguments.

    .. code-block:: python

        >>> calldata = Token[0].transfer.encode_input(accounts[1], 1000)
        0xa9059cbb0000000000000000000000000d36bdba474b5b442310a5bfb989903020249bba00000000000000000000000000000000000000000000000000000000000003e8
        >>> accounts[0].transfer(Token[0], 0, data=calldata)

        Transaction sent: 0x8dbf15878104571669f9843c18afc40529305ddb842f94522094454dcde22186
        Token.transfer confirmed - block: 2   gas used: 50985 (100.00%)
        <Transaction object '0x8dbf15878104571669f9843c18afc40529305ddb842f94522094454dcde22186'>


.. py:classmethod:: ContractTx.decode_output(hexstr)

    Decodes raw hexstring data returned by this method.

    .. code-block:: python

        >>>  Token[0].balanceOf.decode_output("0x00000000000000000000000000000000000000000000003635c9adc5dea00000")
        1000000000000000000000


OverloadedMethod
----------------

.. py:class:: brownie.network.contract.OverloadedMethod(address, name, owner)

    When a contract uses `overloaded function names <https://solidity.readthedocs.io/en/latest/contracts.html#function-overloading>`_, the ``ContractTx`` or ``ContractCall`` objects are stored inside a dict-like ``OverloadedMethod`` container.

    .. code-block:: python

        >>> erc223 = ERC223Token[0]
        >>> erc223.transfer
        <OverloadedMethod object 'ERC223Token.transfer'>

    Individual methods are mapped to keys that correspond to the function input types. Input types can be given as a single comma-seperated string or a tuple of strings. ``uint`` and ``uint256`` are equivalent.

    .. code-block:: python

        >>> erc223.transfer['address,uint']
        <ContractTx object 'transfer(address,uint256)'>

        >>> erc223.transfer['address', 'uint256', 'uint256']
        <ContractTx object 'transfer(address,uint256,uint256)'>



``brownie.network.event``
=========================

The ``event`` module contains classes and methods related to decoding transaction event logs. It is largely a wrapper around `eth-event <https://github.com/iamdefinitelyahuman/eth-event>`__.

Brownie stores encrypted event topics in ``brownie/data/topics.json``. The JSON file is loaded when this module is imported.

.. _api-network-eventdict:

EventDict
---------

.. py:class:: brownie.types.types.EventDict

    Hybrid container type that works as a `dict <https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>`__ and a `list <https://docs.python.org/3/library/stdtypes.html#lists>`__. Base class, used to hold all events that are fired in a transaction.

    When accessing events inside the object:

    * If the key is given as an integer, events are handled as a list in the order that they fired. An ``_EventItem`` is returned for the specific event that fired at the given position.
    * If the key is given as a string, a ``_EventItem`` is returned that contains all the events with the given name.

    .. code-block:: python

        >>> tx
        <Transaction object '0xf1806643c21a69fcfa29187ea4d817fb82c880bcd7beee444ef34ea3b207cebe'>
        >>> tx.events
        {
            'CountryModified': [
                {
                    'country': 1,
                    'limits': (0, 0, 0, 0, 0, 0, 0, 0),
                    'minrating': 1,
                    'permitted': True
                },
                    'country': 2,
                    'limits': (0, 0, 0, 0, 0, 0, 0, 0),
                    'minrating': 1,
                    'permitted': True
                }
            ],
            'MultiSigCallApproved': {
                'callHash': "0x0013ae2e37373648c5161d81ca78d84e599f6207ad689693d6e5938c3ae4031d",
                'caller': "0xf9c1fd2f0452fa1c60b15f29ca3250dfcb1081b9"
            }
        }
        >>> tx.events['CountryModified']
        [
            {
                'country': 1,
                'limits': (0, 0, 0, 0, 0, 0, 0, 0),
                'minrating': 1,
                'permitted': True
            },
                'country': 2,
                'limits': (0, 0, 0, 0, 0, 0, 0, 0),
                'minrating': 1,
                'permitted': True
            }
        ]
        >>> tx.events[0]
        {
            'callHash': "0x0013ae2e37373648c5161d81ca78d84e599f6207ad689693d6e5938c3ae4031d",
            'caller': "0xf9c1fd2f0452fa1c60b15f29ca3250dfcb1081b9"
        }

.. py:classmethod:: EventDict.count(name)

    Returns the number of events that fired with the given name.

    .. code-block:: python

        >>> tx.events.count('CountryModified')
        2

.. py:classmethod:: EventDict.items

    Returns a set-like object providing a view on the object's items.

.. py:classmethod:: EventDict.keys

    Returns a set-like object providing a view on the object's keys.

.. py:classmethod:: EventDict.values

    Returns an object providing a view on the object's values.

Internal Classes and Methods
----------------------------

_EventItem
**********

.. py:class:: brownie.types.types._EventItem

    Hybrid container type that works as a `dict <https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>`__ and a `list <https://docs.python.org/3/library/stdtypes.html#lists>`__. Represents one or more events with the same name that were fired in a transaction.

    Instances of this class are created by ``EventDict``, it is not intended to be instantiated directly.

    When accessing events inside the object:

    * If the key is given as an integer, events are handled as a list in the order that they fired. An ``_EventItem`` is returned for the specific event that fired at the given position.
    * If the key is given as a string, ``_EventItem`` assumes that you wish to access the first event contained within the object. ``event['value']`` is equivalent to ``event[0]['value']``.

    All values within the object are formatted by methods outlined in the :ref:`convert<api-brownie-convert>` module.

    .. code-block:: python

        >>> event = tx.events['CountryModified']
        <Transaction object '0xf1806643c21a69fcfa29187ea4d817fb82c880bcd7beee444ef34ea3b207cebe'>
        >>> event
        [
            {
                'country': 1,
                'limits': (0, 0, 0, 0, 0, 0, 0, 0),
                'minrating': 1,
                'permitted': True
            },
                'country': 2,
                'limits': (0, 0, 0, 0, 0, 0, 0, 0),
                'minrating': 1,
                'permitted': True
            }
        ]
        >>> event[0]
        {
            'country': 1,
            'limits': (0, 0, 0, 0, 0, 0, 0, 0),
            'minrating': 1,
            'permitted': True
        }
        >>> event['country']
        1
        >>> event[1]['country']
        2

.. py:attribute:: _EventItem.name

    The name of the event(s) contained within this object.

    .. code-block:: python

        >>> tx.events[2].name
        CountryModified


.. py:attribute:: _EventItem.pos

    A tuple giving the absolute position of each event contained within this object.

    .. code-block:: python

        >>> event.pos
        (1, 2)
        >>> event[1].pos
        (2,)
        >>> tx.events[2] == event[1]
        True

.. py:classmethod:: _EventItem.items

    Returns a set-like object providing a view on the items in the first event within this object.

.. py:classmethod:: _EventItem.keys

    Returns a set-like object providing a view on the keys in the first event within this object.

.. py:classmethod:: _EventItem.values

    Returns an object providing a view on the values in the first event within this object.

Internal Methods
****************

.. py:method:: brownie.network.event._get_topics(abi)

    Generates encoded topics from the given ABI, merges them with those already known in ``topics.json``, and returns a dictioary in the form of ``{'Name': "encoded topic hexstring"}``.

    .. code-block:: python

        >>> from brownie.network.event import _get_topics
        >>> abi = [{'name': 'Approval', 'anonymous': False, 'type': 'event', 'inputs': [{'name': 'owner', 'type': 'address', 'indexed': True}, {'name': 'spender', 'type': 'address', 'indexed': True}, {'name': 'value', 'type': 'uint256', 'indexed': False}]}, {'name': 'Transfer', 'anonymous': False, 'type': 'event', 'inputs': [{'name': 'from', 'type': 'address', 'indexed': True}, {'name': 'to', 'type': 'address', 'indexed': True}, {'name': 'value', 'type': 'uint256', 'indexed': False}]}]
        >>> _get_topics(abi)
        {'Transfer': '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef', 'Approval': '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'}


.. py:method:: brownie.network.event._decode_logs(logs)

    Given an array of logs as returned by ``eth_getLogs`` or ``eth_getTransactionReceipt`` RPC calls, returns an :ref:`api-network-eventdict`.

    .. code-block:: python

        >>> from brownie.network.event import _decode_logs
        >>> tx = Token[0].transfer(accounts[1], 100)

        Transaction sent: 0xfefc3b7d912ed438b312414fb31d94ff757970f4d2e74dd0950d5c58cc23fdb1
        Token.transfer confirmed - block: 2   gas used: 50993 (33.77%)
        <Transaction object '0xfefc3b7d912ed438b312414fb31d94ff757970f4d2e74dd0950d5c58cc23fdb1'>
        >>> e = _decode_logs(tx.logs)
        >>> repr(e)
        <brownie.types.types.EventDict object at 0x7feed74aebe0>
        >>> e
        {
            'Transfer': {
                'from': "0x1ce57af3672a16b1d919aeb095130ab288ca7456",
                'to': "0x2d72c1598537bcf4a4af97668b3a24e68b7d0cc5",
                'value': 100
            }
        }

.. py:method:: brownie.network.event._decode_trace(trace)

    Given the ``structLog`` from a ``debug_traceTransaction`` RPC call, returns an :ref:`api-network-eventdict`.

    .. code-block:: python

        >>> from brownie.network.event import _decode_trace
        >>> tx = Token[0].transfer(accounts[2], 1000, {'from': accounts[3]})

        Transaction sent: 0xc6365b065492ea69ad3cbe26039a45a68b2e9ab9d29c2ff7d5d9162970b176cd
        Token.transfer confirmed (Insufficient Balance) - block: 2   gas used: 23602 (19.10%)
        <Transaction object '0xc6365b065492ea69ad3cbe26039a45a68b2e9ab9d29c2ff7d5d9162970b176cd'>
        >>> e = _decode_trace(tx.trace)
        >>> repr(e)
        <brownie.types.types.EventDict object at 0x7feed74aebe0>
        >>> e
        {}

.. _api-network-history:

``brownie.network.state``
=========================

The ``state`` module contains classes to record transactions and contracts as they occur on the blockchain.

TxHistory
---------

.. py:class:: brownie.network.state.TxHistory

    List-like :ref:`Singleton<api-types-singleton>` container that contains :ref:`api-network-tx` objects. Whenever a transaction is broadcast, the ``TransactionReceipt`` is automatically added.

    .. code-block:: python

        >>> from brownie.network.state import TxHistory
        >>> history = TxHistory()
        >>> history
        []
        >>> dir(history)
        [copy, from_sender, of_address, to_receiver]


TxHistory Attributes
********************

.. _api-network-history-gas-profile:

.. py:attribute:: TxHistory.gas_profile

    A dict that tracks gas cost statistics for contract function calls over time.

    .. code-block:: python

        >>> history.gas_profile
        {
            'Token.constructor': {
                'avg': 742912,
                'count': 1,
                'high': 742912,
                'low': 742912
            },
            'Token.transfer': {
                'avg': 43535,
                'count': 2,
                'high': 51035,
                'low': 36035
            }
        }

TxHistory Methods
*****************

.. py:classmethod:: TxHistory.copy

    Returns a shallow copy of the object as a ``list``.

    .. code-block:: python

        >>> history
        [<Transaction object '0xe803698b0ade1598c594b2c73ad6a656560a4a4292cc7211b53ffda4a1dbfbe8'>]
        >>> c = history.copy()
        >>> c
        [<Transaction object '0xe803698b0ade1598c594b2c73ad6a656560a4a4292cc7211b53ffda4a1dbfbe8'>]
        >>> type(c)
        <class 'list'>

.. py:classmethod:: TxHistory.from_sender(account)

    Returns a list of transactions where the sender is ``account``.

    .. code-block:: python

        >>> history.from_sender(accounts[1])
        [<Transaction object '0xe803698b0ade1598c594b2c73ad6a656560a4a4292cc7211b53ffda4a1dbfbe8'>]

.. py:classmethod:: TxHistory.to_receiver(account)

    Returns a list of transactions where the receiver is ``account``.

    .. code-block:: python

        >>> history.to_receiver(accounts[2])
        [<Transaction object '0xe803698b0ade1598c594b2c73ad6a656560a4a4292cc7211b53ffda4a1dbfbe8'>]

.. py:classmethod:: TxHistory.of_address(account)

    Returns a list of transactions where ``account`` is the sender or receiver.

    .. code-block:: python

        >>> history.of_address(accounts[1])
        [<Transaction object '0xe803698b0ade1598c594b2c73ad6a656560a4a4292cc7211b53ffda4a1dbfbe8'>]

TxHistory Internal Methods
**************************

.. py:classmethod:: TxHistory._reset()

    Called by :ref:`rpc._notify_registry <api-network-rpc-notify-registry>` when the local chain has been reset. All ``TransactionReceipt`` objects are removed from the container.

.. py:classmethod:: TxHistory._revert(height)

    Called by :ref:`rpc._notify_registry <api-network-rpc-notify-registry>` when the local chain has been reverted to a block height greater than zero. Any ``TransactionReceipt`` objects that no longer exist are removed from the container.


Internal Methods
----------------

The internal methods in the ``state`` module are primarily used for tracking and adjusting ``Contract`` instances whenever the local RPC network is reverted or reset.

.. py:method:: brownie.network.state._add_contract(contract)

    Adds a ``Contract`` or ``ProjectContract`` object to the global contract record.

.. py:method:: brownie.network.state._find_contract(address)

    Given an address, returns the related ``Contract`` or ``ProjectContract`` object. If none exists, returns ``None``.

    This method is used internally by Brownie to locate a ``ProjectContract`` when the project it belongs to is unknown.

.. py:method:: brownie.network.state._remove_contract(contract)

    Removes a ``Contract`` or ``ProjectContract`` object to the global contract record.

.. py:method:: brownie.network.state._get_current_dependencies()

    Returns a list of the names of all currently deployed contracts, and of every contract that these contracts are dependent upon.

    Used during testing to determine which contracts must change before a test needs to be re-run.

``brownie.network.rpc``
=======================

The ``rpc`` module contains the ``Rpc`` class, which is used to interact with ``ganache-cli`` when running a local RPC environment.

.. note:: Account balances, contract containers and transaction history are automatically modified when the local RPC is terminated, reset or reverted.

.. _rpc:

Rpc
---

.. py:class:: brownie.network.rpc.Rpc

    :ref:`Singleton<api-types-singleton>` object for interacting with ``ganache-cli`` when running a local RPC environment. When using the console or writing tests, an instance of this class is available as ``rpc``.

    .. code-block:: python

        >>> from brownie import rpc
        >>> rpc
        <lib.components.eth.Rpc object at 0x7ffb7cbab048>
        >>> dir(rpc)
        [is_active, kill, launch, mine, reset, revert, sleep, snapshot, time]

Rpc Methods
***********

.. py:classmethod:: Rpc.launch(cmd)

    Launches the local RPC client as a `subprocess <https://docs.python.org/3/library/subprocess.html#subprocess.Popen>`_. ``cmd`` is the command string requiried to run it.

    If the process cannot load successfully, raises ``brownie.RPCProcessError``.

    If a provider has been set in ``Web3`` but is unable to connect after launching, raises a ``brownie.RPCConnectionError``.

    .. code-block:: python

        >>> rpc.launch('ganache-cli')
        Launching 'ganache-cli'...

.. py:classmethod:: Rpc.attach(laddr)

    Attaches to an already running RPC client.

    ``laddr``: Address that the client is listening at. Can be supplied as a string ``"http://127.0.0.1:8545"`` or tuple ``("127.0.0.1", 8545)``.

    Raises a ``ProcessLookupError`` if the process cannot be found.

    .. code-block:: python

        >>> rpc.attach('http://127.0.0.1:8545')

.. py:classmethod:: Rpc.kill(exc=True)

    Kills the RPC subprocess. Raises ``SystemError`` if ``exc`` is ``True`` and the RPC is not currently active.

    .. code-block:: python

        >>> rpc.kill()
        Terminating local RPC client...

    .. note:: Brownie registers this method with the `atexit <https://docs.python.org/3/library/atexit.html>`_ module. It is not necessary to explicitly kill ``Rpc`` before terminating a script or console session.

.. py:classmethod:: Rpc.reset()

    Resets the RPC to the genesis state by loading a snapshot. This is NOT equivalent to calling ``rpc.kill`` and then ``rpc.launch``.

    .. code-block:: python

        >>> rpc.reset()

.. py:classmethod:: Rpc.is_active()

    Returns a boolean indicating if the RPC process is currently active.

    .. code-block:: python

        >>> rpc.is_active()
        False
        >>> rpc.launch()
        >>> rpc.is_active()
        True

.. py:classmethod:: Rpc.is_child()

    Returns a boolean indicating if the RPC process is a child process of Brownie. If the RPC is not currently active, returns ``False``.

    .. code-block:: python

        >>> rpc.is_child()
        True

.. py:classmethod:: Rpc.evm_version()

    Returns the currently active EVM version as a string.

    .. code-block:: python

        >>> rpc.evm_version()
        'petersburg'

.. py:classmethod:: Rpc.evm_compatible(version)

    Returns a boolean indicating if the given ``version`` is compatible with the currently active EVM version.

    .. code-block:: python

        >>> rpc.evm_compatible('byzantium')
        True

.. py:classmethod:: Rpc.time()

    Returns the current epoch time in the RPC as an integer.

    .. code-block:: python

        >>> rpc.time()
        1550189043

.. py:classmethod:: Rpc.sleep(seconds)

    Advances the RPC time. You can only advance the time by whole seconds.

    .. code-block:: python

        >>> rpc.time()
        1550189043
        >>> rpc.sleep(100)
        >>> rpc.time()
        1550189143

.. py:classmethod:: Rpc.mine(blocks=1)

    Forces new blocks to be mined.

    .. code-block:: python

        >>> web3.eth.blockNumber
        0
        >>> rpc.mine()
        Block height at 1
        >>> web3.eth.blockNumber
        1
        >>> rpc.mine(3)
        Block height at 4
        >>> web3.eth.blockNumber
        4

.. py:classmethod:: Rpc.snapshot()

    Creates a snapshot at the current block height.

    .. code-block:: python

        >>> rpc.snapshot()
        Snapshot taken at block height 4

.. py:classmethod:: Rpc.revert()

    Reverts the blockchain to the latest snapshot. Raises ``ValueError`` if no snapshot has been taken.

    .. code-block:: python

        >>> rpc.snapshot()
        Snapshot taken at block height 4
        >>> accounts[0].balance()
        100000000000000000000
        >>> accounts[0].transfer(accounts[1], "10 ether")

        Transaction sent: 0xd5d3b40eb298dfc48721807935eda48d03916a3f48b51f20bcded372113e1dca
        Transaction confirmed - block: 5   gas used: 21000 (100.00%)
        <Transaction object '0xd5d3b40eb298dfc48721807935eda48d03916a3f48b51f20bcded372113e1dca'>
        >>> accounts[0].balance()
        89999580000000000000
        >>> rpc.revert()
        Block height reverted to 4
        >>> accounts[0].balance()
        100000000000000000000

Rpc Internal Methods
********************

.. py:classmethod:: Rpc._internal_snap()

    Takes an internal snapshot at the current block height.

.. py:classmethod:: Rpc._internal_revert()

    Reverts to the most recently taken internal snapshot.

    .. note::

        When calling this method, you must ensure that the user has not had a chance to take their own snapshot since ``_internal_snap`` was called.

Internal Methods
----------------

.. py:class:: brownie.network.rpc._revert_register(obj)

    Registers an object to be called whenever the local RPC is reset or reverted. Objects that register must include ``_revert`` and ``_reset`` methods in order to receive these callbacks.

.. _api-network-rpc-notify-registry:

.. py:class:: brownie.network.rpc._notify_registry(height)

    Calls each registered object's ``_revert`` or ``_reset`` method after the local state has been reverted.


``brownie.network.transaction``
===============================

The ``transaction`` module contains the ``TransactionReceipt`` class and related internal methods.

.. _api-network-tx:

TransactionReceipt
------------------

.. py:class:: brownie.network.transaction.TransactionReceipt

    An instance of this class is returned whenever a transaction is broadcasted. When printed in the console, the transaction hash will appear yellow if the transaction is still pending or red if the transaction caused the EVM to revert.

    Many of the attributes return ``None`` while the transaction is still pending.

    .. code-block:: python

        >>> tx = Token[0].transfer
        <ContractTx object 'transfer(address,uint256)'>
        >>> Token[0].transfer(accounts[1], 100000, {'from':accounts[0]})

        Transaction sent: 0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0
        Transaction confirmed - block: 2   gas spent: 51049
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> dir(tx)
        [block_number, call_trace, contract_address, contract_name, error, events, fn_name, gas_limit, gas_price, gas_used, info, input, logs, nonce, receiver, sender, status, txid, txindex, value]

TransactionReceipt Attributes
*****************************

.. py:attribute:: TransactionReceipt.block_number

    The block height at which the transaction confirmed.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.block_number
        2

.. py:attribute:: TransactionReceipt.contract_address

    The address of the contract deployed as a result of this transaction, if any.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.contract_address
        None

.. py:attribute:: TransactionReceipt.contract_name

    The name of the contract that was called or deployed in this transaction.

    .. code-block:: python

        >>> tx
        <Transaction object '0xcdd07c6235bf093e1f30ac393d844550362ebb9b314b7029667538bfaf849749'>
        >>> tx.contract_name
        Token

.. py:attribute:: TransactionReceipt.events

    An :ref:`api-network-eventdict` of decoded event logs for this transaction.

    .. note:: If you are connected to an RPC client that allows for ``debug_traceTransaction``, event data is still available when the transaction reverts.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.events
        {
            'Transfer': {
                'from': "0x94dd96c7e6012c927537cd789c48c42a1d1f790d",
                'to': "0xc45272e89a23d1a15a24041bce7bc295e79f2d13",
                'value': 100000
            }
        }

.. py:attribute:: TransactionReceipt.fn_name

    The name of the function called by the transaction.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.fn_name
        'transfer'

.. py:attribute:: TransactionReceipt.gas_limit

    The gas limit of the transaction, in wei as an ``int``.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.gas_limit
        150921

.. py:attribute:: TransactionReceipt.gas_price

    The gas price of the transaction, in wei as an ``int``.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.gas_price
        2000000000

.. py:attribute:: TransactionReceipt.gas_used

    The amount of gas consumed by the transaction, in wei as an ``int``.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.gas_used
        51049

.. py:attribute:: TransactionReceipt.input

    The complete calldata of the transaction as a hexstring.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.input
        '0xa9059cbb00000000000000000000000031d504908351d2d87f3d6111f491f0b52757b592000000000000000000000000000000000000000000000000000000000000000a'


.. py:attribute:: TransactionReceipt.logs

    The raw event logs for the transaction. Not available if the transaction reverts.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.logs
        [AttributeDict({'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xa8afb59a850adff32548c65041ec253eb64e1154042b2e01e2cd8cddb02eb94f'), 'blockHash': HexBytes('0x0b93b4cf230c9ef92b990de9cd62611447d83d396f1b13204d26d28bd949543a'), 'blockNumber': 6, 'address': '0x79447c97b6543F6eFBC91613C655977806CB18b0', 'data': '0x0000000000000000000000006b5132740b834674c3277aafa2c27898cbe740f600000000000000000000000031d504908351d2d87f3d6111f491f0b52757b592000000000000000000000000000000000000000000000000000000000000000a', 'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef')], 'type': 'mined'})]

.. py:attribute:: TransactionReceipt.modified_state

    Boolean indicating if this transaction resuled in any state changes on the blockchain.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.modified_state
        True

.. py:attribute:: TransactionReceipt.nonce

    The nonce of the transaction.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.nonce
        2

.. py:attribute:: TransactionReceipt.receiver

    The address the transaction was sent to, as a string.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.receiver
        '0x79447c97b6543F6eFBC91613C655977806CB18b0'

.. py:attribute:: TransactionReceipt.revert_msg

    The error string returned when a transaction causes the EVM to revert, if any.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.revert_msg
        None

.. py:attribute:: TransactionReceipt.return_value

    The value returned from the called function, if any. Only available if the RPC client allows ``debug_traceTransaction``.

    If more then one value is returned, they are stored in a :ref:`ReturnValue<return_value>`.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.return_value
        True

.. py:attribute:: TransactionReceipt.sender

    The address the transaction was sent from. Where possible, this will be an Account instance instead of a string.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.sender
        <Account object '0x6B5132740b834674C3277aAfa2C27898CbE740f6'>

.. py:attribute:: TransactionReceipt.status

    The status of the transaction: -1 for pending, 0 for failed, 1 for success.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.status
        1

.. py:attribute:: TransactionReceipt.trace

    An expanded `transaction trace <https://github.com/ethereum/go-ethereum/wiki/Tracing:-Introduction#user-content-basic-traces>`_ structLog, returned from the `debug_traceTransaction <https://github.com/ethereum/go-ethereum/wiki/Management-APIs#user-content-debug_tracetransaction>`__ RPC endpoint. If you are using Infura this attribute is not available.

    Along with the standard data, the structLog also contains the following additional information:

    * ``address``: The address of the contract that executed this opcode
    * ``contractName``: The name of the contract
    * ``fn``: The name of the function
    * ``jumpDepth``: The number of jumps made since entering this contract. The initial function has a value of 1.
    * ``source``: The path and offset of the source code associated with this opcode.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> len(tx.trace)
        239
        >>> tx.trace[0]
        {
            'address': "0x79447c97b6543F6eFBC91613C655977806CB18b0",
            'contractName': "Token",
            'depth': 0,
            'error': "",
            'fn': "Token.transfer",
            'gas': 128049,
            'gasCost': 22872,
            'jumpDepth': 1,
            'memory': [],
            'op': "PUSH1",
            'pc': 0,
            'source': {
                'filename': "contracts/Token.sol",
                'offset': [53, 2053]
            },
            'stack': [],
            'storage': {
            }
        }

.. py:attribute:: TransactionReceipt.txid

    The transaction hash.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.txid
        '0xa8afb59a850adff32548c65041ec253eb64e1154042b2e01e2cd8cddb02eb94f'

.. py:attribute:: TransactionReceipt.txindex

    The integer of the transaction's index position in the block.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.txindex
        0

.. py:attribute:: TransactionReceipt.value

    The value of the transaction, in  :ref:`wei<wei>`.

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.value
        0

TransactionReceipt Methods
**************************

.. py:classmethod:: TransactionReceipt.info()

    Displays verbose information about the transaction, including event logs and the error string if a transaction reverts.

    .. code-block:: python

        >>> tx = accounts[0].transfer(accounts[1], 100)
        <Transaction object '0x2facf2d1d2fdfa10956b7beb89cedbbe1ba9f4a2f0592f8a949d6c0318ec8f66'>
        >>> tx.info()

        Transaction was Mined
        ---------------------
        Tx Hash: 0x2facf2d1d2fdfa10956b7beb89cedbbe1ba9f4a2f0592f8a949d6c0318ec8f66
        From: 0x5fe657e72E76E7ACf73EBa6FA07ecB40b7312d80
        To: 0x5814fC82d51732c412617Dfaecb9c05e3B823253
        Value: 100
        Block: 1
        Gas Used: 21000

           Events In This Transaction
           --------------------------
           Transfer
              from: 0x5fe657e72E76E7ACf73EBa6FA07ecB40b7312d80
              to: 0x31d504908351d2d87f3d6111f491f0b52757b592
              value: 100

.. py:classmethod:: TransactionReceipt.call_trace()

    Returns the sequence of contracts and functions called while executing this transaction, and the step indexes where each new method is entered and exitted. Any functions that terminated with ``REVERT`` or ``INVALID`` opcodes are highlighted in red.

    .. code-block:: python

        >>> tx = Token[0].transferFrom(accounts[2], accounts[3], "10000 ether")

        Transaction sent: 0x0d96e8ceb555616fca79dd9d07971a9148295777bb767f9aa5b34ede483c9753
        Token.transferFrom confirmed (reverted) - block: 4   gas used: 25425 (26.42%)

        >>> tx.call_trace()
        Call trace for '0x0d96e8ceb555616fca79dd9d07971a9148295777bb767f9aa5b34ede483c9753':
        Token.transfer 0:244  (0x4A32104371b05837F2A36dF6D850FA33A92a178D)
        └─Token.transfer 72:226
          ├─SafeMath.sub 100:114
          └─SafeMath.add 149:165

.. py:classmethod:: TransactionReceipt.traceback()

    Returns an error traceback for the transaction, similar to a regular python traceback. If the transaction did not revert, returns an empty string.

    .. code-block:: python

        >>> tx = >>> Token[0].transfer(accounts[1], "100000 ether")

        Transaction sent: 0x9542e92a904e9d345def311ea52f22c3191816c6feaf7286f9b48081ab255ffa
        Token.transfer confirmed (reverted) - block: 5   gas used: 23956 (100.00%)
        <Transaction object '0x9542e92a904e9d345def311ea52f22c3191816c6feaf7286f9b48081ab255ffa'>

        >>> tx.traceback()
        Traceback for '0x9542e92a904e9d345def311ea52f22c3191816c6feaf7286f9b48081ab255ffa':
        Trace step 99, program counter 1699:
          File "contracts/Token.sol", line 67, in Token.transfer:
            balances[msg.sender] = balances[msg.sender].sub(_value);
        Trace step 110, program counter 1909:
          File "contracts/SafeMath.sol", line 9, in SafeMath.sub:
            require(b <= a);

.. py:classmethod:: TransactionReceipt.error(pad=3)

    Displays the source code that caused the first revert in the transaction, if any.

    * ``pad``: Number of unrelated liness of code to include before and after the relevant source


    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.error()
        Source code for trace step 86:
          File "contracts/SafeMath.sol", line 9, in SafeMath.sub:

                c = a + b;
                require(c >= a);
            }
            function sub(uint a, uint b) internal pure returns (uint c) {
                require(b <= a);
                c = a - b;
            }
            function mul(uint a, uint b) internal pure returns (uint c) {
                c = a * b;

.. py:classmethod:: TransactionReceipt.source(idx, pad=3)

    Displays the associated source code for a given stack trace step.

    * ``idx``: Stack trace step index
    * ``pad``: Number of unrelated liness of code to include before and after the relevant source

    .. code-block:: python

        >>> tx
        <Transaction object '0xac54b49987a77805bf6bdd78fb4211b3dc3d283ff0144c231a905afa75a06db0'>
        >>> tx.source(86)
        Source code for trace step 86:
          File "contracts/SafeMath.sol", line 9, in SafeMath.sub:

                c = a + b;
                require(c >= a);
            }
            function sub(uint a, uint b) internal pure returns (uint c) {
                require(b <= a);
                c = a - b;
            }
            function mul(uint a, uint b) internal pure returns (uint c) {
                c = a * b;

``brownie.network.web3``
========================

The ``web3`` module contains a slightly modified version of the web3.py ``Web3`` class that is used throughout various Brownie modules for RPC communication.

.. _web3:

Web3
----

See the `Web3 API documentation <https://web3py.readthedocs.io/en/stable/web3.main.html#web3.Web3>`_ for detailed information on all the methods and attributes available here. This document only outlines methods that differ from the normal ``Web3`` public interface.

.. py:class:: brownie.network.web3.Web3

    Brownie subclass of ``Web3``. An instance is created at ``brownie.network.web3.web`` and available for import from the main package.

    .. code-block:: python

        >>> from brownie import web3
        >>>

Web3 Methods
************

.. py:classmethod:: Web3.connect(uri)

    Connects to a `provider <https://web3py.readthedocs.io/en/stable/providers.html>`_. ``uri`` can be the path to a local IPC socket, a websocket address beginning in ``ws://`` or a URL.

    .. code-block:: python

        >>> web3.connect('https://127.0.0.1:8545')
        >>>

.. py:classmethod:: Web3.disconnect()

    Disconnects from a provider.

    .. code-block:: python

        >>> web3.disconnect()
        >>>

Web3 Attributes
***************

.. py:classmethod:: Web3.genesis_hash

    Returns the hash of the genesis block for the active chain, as a string without a `0x` prefix.

    .. code-block:: python

        >>> web3.genesis_hash
        '41941023680923e0fe4d74a34bdac8141f2540e3ae90623718e47d66d1ca4a2d'


Web3 Internals
**************

.. py:attribute:: Web3._mainnet

    Provides access to a ``Web3`` instance connected to the ``mainnet`` network as defined in the configuration file. Used internally for `ENS <https://ens.domains/>`_ and `ethPM <https://www.ethpm.com/>`_ lookups.

    Raises ``MainnetUndefined`` if the ``mainnet`` network is not defined.

Internal Methods
----------------

.. py:method:: brownie.network.web3._resolve_address(address)

    Used internally for standardizing address inputs. If ``address`` is a string containing a ``.`` Brownie will attempt to resolve an `ENS domain name <https://ens.domains/>`_ address. Otherwise, returns the result of :ref:`brownie.convert.to_address<api-brownie-convert-address>`.
