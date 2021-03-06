USE [DouBan]
GO
/****** Object:  User [syy1]    Script Date: 04/26/2019 17:52:08 ******/
CREATE USER [syy1] FOR LOGIN [syy1] WITH DEFAULT_SCHEMA=[db_accessadmin]
GO
/****** Object:  Table [dbo].[Movies]    Script Date: 04/26/2019 17:52:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[Movies](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[moviename] [varchar](50) NOT NULL,
	[moviegrades] [varchar](50) NOT NULL,
	[movieassess] [varchar](50) NOT NULL,
	[movieshortassess] [varchar](max) NULL,
 CONSTRAINT [PK_Movies] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_PADDING OFF
GO
