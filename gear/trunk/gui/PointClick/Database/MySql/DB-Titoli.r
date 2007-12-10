#
# NOTA: le operazioni se non altrimenti specificato vengono fatte su singoli titoli
#
#
# Scarica/aggiorna da Yahoo 
# Aggiorna tutti i titoli 
#
# Lista titoli
#
# Restituisce un dataframe col titolo in questione
#
# 



YahooDownloadStocksToDatabase<-function(conn,titoli,StartDate="2000-01-03",EndDate,cadenza="d"){

	n<-length(titoli$simbolo);
	zz<-url("http://it.finance.yahoo.com")
	if(inherits(try(open(zz), silent = TRUE),"try-error")) {return();}

	for(i in 1:n){
			
		if(!inherits(try(dati<-get.hist.quote(instrument =titoli$simbolo[i], start = StartDate,end=EndDate,quote = c("High","Low","Open","Close","Volume","AdjClose"),compression=cadenza),silent=TRUE),'try-error'))
		{
			IDTitolo<-mysqlQuickSQL(conn, paste("SELECT IDTitolo FROM listatitoli WHERE Tick1= \'",titoli$simbolo[i],"\'",sep=''))
			DATI<-as.data.frame(dati)
			temp<-as.data.frame(cbind(IDTitolo,as.character(index(dati))))
			DATI<-data.frame(cbind(temp,DATI))
			out<-mysqlWriteTable(conn, 'quotazionititoli', DATI, row.names = FALSE,append=TRUE)
		}
		else{next}
	}
	close(zz)

	return(out)
}




YahooUpdateStocksToDatabase<-function(conn,titoli,EndDate,cadenza="d"){

	n<-length(titoli$simbolo);
	zz<-url("http://it.finance.yahoo.com")
	if(inherits(try(open(zz), silent = TRUE),"try-error")) {return();}


	for(i in 1:n){
		
		IDTitolo<-mysqlQuickSQL(conn, paste("SELECT IDTitolo FROM listatitoli WHERE Tick1= \'",titoli$simbolo[i],"\'",sep=''))
		MaxDate<-mysqlQuickSQL(conn, paste("SELECT MAX(Date) FROM quotazionititoli WHERE IDTitolo= \'",IDTitolo,"\'",sep=''))
		MaxDate<-as.Date(as.character(MaxDate))
		StartDate<-MaxDate+1;

		if(!inherits(try(dati<-get.hist.quote(instrument =titoli$simbolo[i], start = StartDate,end=EndDate,quote = c("High","Low","Open","Close","Volume","AdjClose"),compression=cadenza),silent=TRUE),'try-error'))
		{
			DATI<-as.data.frame(dati)
			temp<-as.data.frame(cbind(IDTitolo,as.character(index(dati))))
			DATI<-data.frame(cbind(temp,DATI))
			out<-mysqlWriteTable(conn, 'quotazionititoli', DATI, row.names = FALSE,append=TRUE)
		}
		else{next}
	}
	close(zz)

	return(out)
}




#FARE IN MODO CHE CARICHI I DIVERSI TIPI DI TITOLI
CaricaTitolo<-function(conn,IDTitolo,StartDate=NULL,EndDate=Sys.Date()){

		Tipo<-mysqlQuickSQL(conn, paste("SELECT Type FROM listatitoli WHERE IDTitolo= \'",IDTitolo,"\'",sep=''))

		if(is.null(StartDate)){
			StartDate<-mysqlQuickSQL(conn, paste("SELECT MIN(Date) FROM quotazionititoli WHERE IDTitolo= \'",IDTitolo,"\'",sep=''))
			StartDate<-as.Date(as.character(StartDate));
		}

		if(Tipo=='Stock'){
			titolo<-mysqlQuickSQL(conn, paste("SELECT Date,High,Low,Open,Close,Volume,AdjClose FROM quotazionititoli WHERE IDTitolo= \'",IDTitolo,"\'",sep=''))
			out<-zoo(as.matrix(titolo[,2:7]),order.by=as.Date(as.character(titolo[,1])))
		}
		else if (Tipo=='Index') {
		}
		#...
		
		return(out)
}





ListaTitoli<-function(conn){
		Titoli<-mysqlQuickSQL(conn,"SELECT Tick1,Description,Type,Nazione,Mercato FROM ListaTitoli")
		return(Titoli)
}



UpdateAll<-function(conn,EndDate=Sys.Date(),cadenza='d'){
		Titoli<-mysqlQuickSQL(conn,"SELECT IDTitolo FROM ListaTitoli")
		for(i in 1:nrow(Titoli))
			YahooUpdateStocksToDatabase(conn,Titoli[i],EndDate=EndDate,cadenza=cadenza)
}


TitoliPerTipo<-function(conn){
	Tit<-mysqlQuickSQL(conTRADE,"SELECT Type FROM ListaTitoli")
	
	tipi<-table(Tit$Type)
	out<-vector(mode='list',length(tipi))
	livelli<-names(tipi)
	for(i in 1:length(livelli)){
		query<-mysqlQuickSQL(conTRADE,paste("SELECT IDTitolo,Description FROM ListaTitoli WHERE Type='",livelli[i],"'",sep=''))
		out[[i]]<-query
	}
	names(out)<-livelli
	return(out)
}

TitoliPerTipo(conTRADE)

