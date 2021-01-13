from iconservice import *


class SampleMultiToken(IconScoreBase):
    def __init__(self, db: 'IconScoreDatabase') -> None:
        super().__init__(db)

    def on_install(self) -> None:
        pass

    def on_update(self) -> None:
        pass

    @external(readonly=True)
    def balanceOf(self, _owner: Address, _id: int) -> int:
        """
        Returns the balance of the owner's tokens.

        :param _owner: the address of the token holder
        :param _id: ID of the token
        :return: the _owner's balance of the token type requested
        """
        pass

    @external(readonly=True)
    def balanceOfBatch(self, _owners: List[Address], _ids: List[int]) -> List[int]:
        """
        Returns the balance of multiple owner/id pairs.

        :param _owners: the addresses of the token holders
        :param _ids: IDs of the tokens
        :return: the list of balance (i.e. balance for each owner/id pair)
        """
        pass

    @external(readonly=True)
    def tokenURI(self, _id: int) -> str:
        """
        Returns an URI for a given token ID.

        :param _id: ID of the token
        :return: the URI string
        """
        pass

    @external
    def transferFrom(self, _from: Address, _to: Address, _id: int, _value: int, _data: bytes = None):
        """
        Transfers `_value` amount of an token `_id` from one address to another address,
        and must emit `TransferSingle` event to reflect the balance change.
        When the transfer is complete, this method must invoke `onIRC31Received(Address,Address,int,int,bytes)` in `_to`,
        if `_to` is a contract. If the `onIRC31Received` method is not implemented in `_to` (receiver contract),
        then the transaction must fail and the transfer of tokens should not occur.
        If `_to` is an externally owned address, then the transaction must be sent without trying to execute
        `onIRC31Received` in `_to`.
        Additional `_data` can be attached to this token transaction, and it should be sent unaltered in call
        to `onIRC31Received` in `_to`. `_data` can be empty.
        Throws unless the caller is the current token holder or the approved address for the token ID.
        Throws if `_from` does not have enough amount to transfer for the token ID.
        Throws if `_to` is the zero address.

        :param _from: source address
        :param _to: target address
        :param _id: ID of the token
        :param _value: the amount of transfer
        :param _data: additional data that should be sent unaltered in call to `_to`
        """
        pass

    @external
    def transferFromBatch(self, _from: Address, _to: Address, _ids: List[int], _values: List[int], _data: bytes = None):
        """
        Transfers `_values` amount(s) of token(s) `_ids` from one address to another address,
        and must emit `TransferSingle` or `TransferBatch` event(s) to reflect all the balance changes.
        When all the transfers are complete, this method must invoke `onIRC31Received(Address,Address,int,int,bytes)` or
        `onIRC31BatchReceived(Address,Address,int[],int[],bytes)` in `_to`,
        if `_to` is a contract. If the `onIRC31Received` method is not implemented in `_to` (receiver contract),
        then the transaction must fail and the transfers of tokens should not occur.
        If `_to` is an externally owned address, then the transaction must be sent without trying to execute
        `onIRC31Received` in `_to`.
        Additional `_data` can be attached to this token transaction, and it should be sent unaltered in call
        to `onIRC31Received` in `_to`. `_data` can be empty.
        Throws unless the caller is the current token holder or the approved address for the token IDs.
        Throws if length of `_ids` is not the same as length of `_values`.
        Throws if `_from` does not have enough amount to transfer for any of the token IDs.
        Throws if `_to` is the zero address.

        :param _from: source address
        :param _to: target address
        :param _ids: IDs of the tokens (order and length must match `_values` list)
        :param _values: transfer amounts per token (order and length must match `_ids` list)
        :param _data: additional data that should be sent unaltered in call to `_to`
        """
        pass

    @external
    def setApprovalForAll(self, _operator: Address, _approved: bool):
        """
        Enables or disables approval for a third party ("operator") to manage all of the caller's tokens,
        and must emit `ApprovalForAll` event on success.

        :param _operator: address to add to the set of authorized operators
        :param _approved: true if the operator is approved, false to revoke approval
        """
        pass

    @external(readonly=True)
    def isApprovedForAll(self, _owner: Address, _operator: Address) -> bool:
        """
        Returns the approval status of an operator for a given owner.

        :param _owner: the owner of the tokens
        :param _operator: the address of authorized operator
        :return: true if the operator is approved, false otherwise
        """
        pass

    @eventlog(indexed=3)
    def TransferSingle(self, _operator: Address, _from: Address, _to: Address, _id: int, _value: int):
        """
        Must trigger on any successful token transfers, including zero value transfers as well as minting or burning.
        When minting/creating tokens, the `_from` must be set to zero address.
        When burning/destroying tokens, the `_to` must be set to zero address.

        :param _operator: the address of an account/contract that is approved to make the transfer
        :param _from: the address of the token holder whose balance is decreased
        :param _to: the address of the recipient whose balance is increased
        :param _id: ID of the token
        :param _value: the amount of transfer
        """
        pass

    @eventlog(indexed=3)
    def TransferBatch(self, _operator: Address, _from: Address, _to: Address, _ids: bytes, _values: bytes):
        """
        Must trigger on any successful token transfers, including zero value transfers as well as minting or burning.
        When minting/creating tokens, the `_from` must be set to zero address.
        When burning/destroying tokens, the `_to` must be set to zero address.

        :param _operator: the address of an account/contract that is approved to make the transfer
        :param _from: the address of the token holder whose balance is decreased
        :param _to: the address of the recipient whose balance is increased
        :param _ids: serialized bytes of list for token IDs (order and length must match `_values`)
        :param _values: serialized bytes of list for transfer amounts per token (order and length must match `_ids`)

        NOTE: RLP (Recursive Length Prefix) would be used for the serialized bytes to represent list type.
        """
        pass

    @eventlog(indexed=2)
    def ApprovalForAll(self, _owner: Address, _operator: Address, _approved: bool):
        """
        Must trigger on any successful approval (either enabled or disabled) for a third party/operator address
        to manage all tokens for the `_owner` address.

        :param _owner: the address of the token holder
        :param _operator: the address of authorized operator
        :param _approved: true if the operator is approved, false to revoke approval
        """
        pass

    @eventlog(indexed=1)
    def URI(self, _id: int, _value: str):
        """
        Must trigger on any successful URI updates for a token ID.
        URIs are defined in RFC 3986.
        The URI must point to a JSON file that conforms to the "ERC-1155 Metadata URI JSON Schema".

        :param _id: ID of the token
        :param _value: the updated URI string
        """
        pass
