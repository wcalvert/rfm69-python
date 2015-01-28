#include "address_server.pb.h"
#include "pb.h"
#include "pb_common.h"
#include "pb_decode.h"
#include "pb_encode.h"
#include "../RFM69/RFM69.h"

#define IDLE					-1
#define DISCOVER_SENT			0
#define DISCOVER_RECEIVED		1
#define OFFER_SENT				2
#define OFFER_RECEIVED			3
#define REQUEST_SENT			4
#define REQUEST_RECEIVED		5
#define ACK_SENT				6
#define ACK_RECEIVED			7

#define MAGIC_NUM				0xfaf

/*class Lease {
protected:
	uint32_t address;
	uint32_t network;
	uint32_t ttl;
	uint32_t startTime;
	uint32_t state;
public:

	Lease(uint32_t address, uint32_t network, uint32_t ttl, uint32_t startTime, uint32_t state)
			: address(address), network(network), ttl(ttl), startTime(startTime), state(state) {
	}

	uint32_t getAddress() const {
		return address;
	}

	void setAddress(uint32_t address) {
		Lease::address = address;
	}

	uint32_t getNetwork() const {
		return network;
	}

	void setNetwork(uint32_t network) {
		Lease::network = network;
	}

	uint32_t getTtl() const {
		return ttl;
	}

	void setTtl(uint32_t ttl) {
		Lease::ttl = ttl;
	}

	uint32_t getStartTime() const {
		return startTime;
	}

	void setStartTime(uint32_t startTime) {
		Lease::startTime = startTime;
	}

	uint32_t getState() const {
		return state;
	}

	void setState(uint32_t state) {
		Lease::state = state;
	}
};
*/
class Message {
public:
	address_server_message message;
	uint8_t buf[128];
//public:
	Message() {
        // provide some kind of default initialization
        //message = {"asdf", 1, 1, 1, 1, 0xfaf};
		/*message.ident = 0xfaf;
        message.offered_address = 1;
        message.network = 1;
        message.ttl = 3600;
        message.type = address_server_message_message_type_DISCOVER;
        //message.uid = "xxxxxxxx";*/
	}

	bool serialize() {
		pb_ostream_t stream = pb_ostream_from_buffer(buf, sizeof(buf));
		return pb_encode(&stream, address_server_message_fields, &message);
	}

	bool deserialize() {
		pb_istream_t stream = pb_istream_from_buffer(buf, sizeof(buf));
		return pb_decode(&stream, address_server_message_fields, &message);
	}

};

class Discover : public Message {
public:
	Discover(const char *uid) {
		message.type = address_server_message_message_type_DISCOVER;
		strcpy(message.uid, uid);
	}
};

class Request : public Message {
public:
	Request(const char *uid, uint32_t address) {
		message.type = address_server_message_message_type_REQUEST;
		strcpy(message.uid, uid);
		message.offered_address = address;
	}
};
/*
class AddrClient {
protected:
	uint32_t state;
	uint32_t address;
	uint32_t network;
	uint32_t ttl;
	uint32_t startTime;
	uint32_t gatewayAddress;
	char uid[10];
	char buf[70];

public:
	AddrClient(const char _uid) {
		//buf = (char *)malloc(sizeof(uint8_t)*70);
		state = IDLE;
		address = 0;
		network = 1;
		ttl = 0;
		startTime = 0;
		gatewayAddress = 1;
		strcpy(uid, _uid);
	}

	bool getLease(RFM69 *radio, uint32_t retries) {
		Discover discover = Discover(uid);
		discover.serialize(buf);
		if(radio->sendWithRetry(gatewayAddress, &buf, strlen(buf))) {
		} else {
			return false;
		}
		return true;
	}


	uint32_t getState() const {
		return state;
	}

	void setState(uint32_t state) {
		AddrClient::state = state;
	}

	uint32_t getAddress() const {
		return address;
	}

	void setAddress(uint32_t address) {
		AddrClient::address = address;
	}

	uint32_t getNetwork() const {
		return network;
	}

	void setNetwork(uint32_t network) {
		AddrClient::network = network;
	}

	uint32_t getTtl() const {
		return ttl;
	}

	void setTtl(uint32_t ttl) {
		AddrClient::ttl = ttl;
	}

	uint32_t getStartTime() const {
		return startTime;
	}

	void setStartTime(uint32_t startTime) {
		AddrClient::startTime = startTime;
	}
};*/
